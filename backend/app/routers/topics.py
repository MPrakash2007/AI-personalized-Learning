from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import random
from typing import List, Optional
from datetime import datetime, timezone

from app.database import get_db
from app.models.learning import Topic, Lesson, LessonStep, Question, TopicProgress, UserQuestionAttempt
from app.models.user import User, LearningStreak, XPTransaction
from app.schemas.learning import (
    TopicResponse, TopicProgressResponse, LessonResponse, QuestionResponse,
    QuizCompleteRequest, QuizCompleteResponse, QuickReferenceResponse
)
from app.auth.deps import get_current_user
from app.services.content_service import get_topic_references
from curriculum import get_topic_quick_reference

router = APIRouter(prefix="/topics", tags=["Topics"])


def _check_topic_accessibility(topic: Topic, user_id: int, db: Session) -> tuple[bool, bool, str]:
    """
    Evaluates whether the user can access this topic sequentially.
    Returns: (is_accessible, is_completed, status)
    """
    user_prog = db.query(TopicProgress).filter(
        TopicProgress.user_id == user_id,
        TopicProgress.topic_id == topic.id
    ).first()

    is_completed = bool(user_prog and user_prog.status in ["COMPLETED", "MASTERED"])

    # Topic 1 in any subject is always accessible
    if topic.order <= 1:
        is_accessible = True
    else:
        # Check previous topic in the same subject
        prev_topic = db.query(Topic).filter(
            Topic.subject_id == topic.subject_id,
            Topic.order == topic.order - 1
        ).first()

        if not prev_topic:
            is_accessible = True
        else:
            prev_prog = db.query(TopicProgress).filter(
                TopicProgress.user_id == user_id,
                TopicProgress.topic_id == prev_topic.id
            ).first()
            is_accessible = bool(prev_prog and prev_prog.status in ["COMPLETED", "MASTERED"])

    if is_completed:
        status = user_prog.status if user_prog else "COMPLETED"
    elif is_accessible:
        status = "AVAILABLE"
    else:
        status = "UPCOMING"

    return is_accessible, is_completed, status


@router.get("/{slug_or_id}")
def get_topic_detail(slug_or_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if slug_or_id.isdigit():
        topic = db.query(Topic).filter(Topic.id == int(slug_or_id)).first()
    else:
        topic = db.query(Topic).filter(Topic.slug == slug_or_id.lower()).first()

    if not topic:
        from app.services.curriculum_seed import ensure_subjects_and_topics
        ensure_subjects_and_topics(db)
        if slug_or_id.isdigit():
            topic = db.query(Topic).filter(Topic.id == int(slug_or_id)).first()
        else:
            topic = db.query(Topic).filter(Topic.slug == slug_or_id.lower()).first()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    from app.services.curriculum_seed import ensure_topic_content_and_questions
    ensure_topic_content_and_questions(db, topic)

    is_accessible, is_completed, status = _check_topic_accessibility(topic, current_user.id, db)

    # Fetch user topic progress
    progress = db.query(TopicProgress).filter(
        TopicProgress.user_id == current_user.id,
        TopicProgress.topic_id == topic.id
    ).first()

    if progress:
        prog_data = TopicProgressResponse(
            topic_id=topic.id,
            status=status,
            mastery_score=progress.mastery_score,
            accuracy=progress.accuracy,
            recent_accuracy=progress.recent_accuracy,
            attempts_count=progress.attempts_count,
            correct_count=progress.correct_count,
            completed_steps=progress.completed_steps,
            total_steps=progress.total_steps,
            last_practiced_at=progress.last_practiced_at,
            next_review_due=progress.next_review_due,
            is_accessible=is_accessible,
            is_completed=is_completed,
            is_current=(is_accessible and not is_completed),
            is_next=(not is_accessible and topic.order == 2)
        )
    else:
        prog_data = TopicProgressResponse(
            topic_id=topic.id,
            status=status,
            mastery_score=0.0,
            accuracy=0.0,
            recent_accuracy=0.0,
            attempts_count=0,
            correct_count=0,
            completed_steps=0,
            total_steps=12,
            is_accessible=is_accessible,
            is_completed=is_completed,
            is_current=(is_accessible and not is_completed),
            is_next=(not is_accessible and topic.order == 2)
        )

    # Fetch lessons and steps
    lessons = db.query(Lesson).filter(Lesson.topic_id == topic.id).order_by(Lesson.order.asc()).all()
    
    # Compile all content sections from the lessons
    sections = []
    for l in lessons:
        steps = db.query(LessonStep).filter(LessonStep.lesson_id == l.id).order_by(LessonStep.step_number.asc()).all()
        for s in steps:
            sections.append({
                "id": s.id,
                "lesson_id": s.lesson_id,
                "step_number": s.step_number,
                "step_type": s.step_type or "concept",
                "section_order": s.section_order or s.step_number,
                "section_type": s.section_type or s.step_type or "concept",
                "title": s.title,
                "content": s.content,
                "code_snippet": s.code_snippet,
                "example_data": s.example_data,
                "diagram_data": s.diagram_data,
                "source_name": s.source_name or "GeeksforGeeks",
                "source_url": s.source_url or "https://www.geeksforgeeks.org",
                "interactive_data": s.interactive_data
            })

    # Fetch questions
    learn_questions = db.query(Question).filter(
        Question.topic_id == topic.id,
        Question.question_context == "LEARN"
    ).all()

    if not learn_questions:
        learn_questions = db.query(Question).filter(Question.topic_id == topic.id).all()

    formatted_questions = [QuestionResponse.model_validate(q) for q in learn_questions]
    source_references = get_topic_references(topic.slug, topic.subject.slug if topic.subject else None)

    return {
        "id": topic.id,
        "subject_id": topic.subject_id,
        "subject_slug": topic.subject.slug if topic.subject else "dbms",
        "subject_name": topic.subject.name if topic.subject else "DBMS",
        "subject_icon": topic.subject.icon if topic.subject else "🗄️",
        "title": topic.title,
        "slug": topic.slug,
        "description": topic.description,
        "order": topic.order,
        "is_boss": topic.is_boss,
        "boss_title": topic.boss_title,
        "progress": prog_data,
        "is_accessible": is_accessible,
        "sections": sections,
        "lessons": [LessonResponse.model_validate(l) for l in lessons],
        "questions": formatted_questions,
        "question_count": len(learn_questions),
        "source_references": source_references
    }


@router.get("/{slug_or_id}/quick-reference", response_model=QuickReferenceResponse)
def get_topic_quick_reference_endpoint(
    slug_or_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns structured exam quick reference data for a topic.
    Powers the Quick Reference modal.
    """
    if slug_or_id.isdigit():
        topic = db.query(Topic).filter(Topic.id == int(slug_or_id)).first()
    else:
        topic = db.query(Topic).filter(Topic.slug == slug_or_id.lower()).first()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    try:
        ref_data = get_topic_quick_reference(topic.slug)
        return QuickReferenceResponse(**ref_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate quick reference: {str(e)}")


@router.get("/{slug_or_id}/learn-questions")
def get_topic_learn_questions(
    slug_or_id: str,
    limit: int = Query(20, ge=1, le=30),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns 15–20 randomized LEARN questions strictly belonging to this topic.
    Guarded by progression: returns 403 if previous topic is not completed.
    """
    if slug_or_id.isdigit():
        topic = db.query(Topic).filter(Topic.id == int(slug_or_id)).first()
    else:
        topic = db.query(Topic).filter(Topic.slug == slug_or_id.lower()).first()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    is_accessible, is_completed, _ = _check_topic_accessibility(topic, current_user.id, db)
    if not is_accessible:
        raise HTTPException(
            status_code=403,
            detail=f"Topic '{topic.title}' is locked. Please complete the previous topic in this subject sequence first."
        )

    # Fetch questions belonging strictly to this topic
    questions = db.query(Question).filter(
        Question.topic_id == topic.id,
        Question.question_context == "LEARN"
    ).all()

    if not questions:
        from app.services.curriculum_seed import ensure_topic_content_and_questions
        ensure_topic_content_and_questions(db, topic)
        questions = db.query(Question).filter(
            Question.topic_id == topic.id,
            Question.question_context == "LEARN"
        ).all()
        if not questions:
            questions = db.query(Question).filter(Question.topic_id == topic.id).all()

    # Shuffle for randomized experience
    q_list = list(questions)
    random.shuffle(q_list)
    selected = q_list[:limit]

    return {
        "topic_id": topic.id,
        "topic_title": topic.title,
        "topic_slug": topic.slug,
        "total_available": len(questions),
        "count": len(selected),
        "questions": [QuestionResponse.model_validate(q) for q in selected]
    }


@router.post("/{slug_or_id}/complete-quiz", response_model=QuizCompleteResponse)
def complete_topic_quiz(
    slug_or_id: str,
    payload: QuizCompleteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Completes the topic quiz:
    - Calculates mastery score and performance tier
    - Updates TopicProgress to COMPLETED or MASTERED
    - Unlocks the next topic in the subject sequence
    - Awards XP and updates streaks
    - Returns details on mastery and unlocked next topic
    """
    if slug_or_id.isdigit():
        topic = db.query(Topic).filter(Topic.id == int(slug_or_id)).first()
    else:
        topic = db.query(Topic).filter(Topic.slug == slug_or_id.lower()).first()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    if payload.score is not None and payload.total is not None:
        score = max(0, payload.score)
        total = max(1, payload.total)
    elif payload.answers is not None and len(payload.answers) > 0:
        total = len(payload.answers)
        score = sum(
            1 for a in payload.answers
            if a.get("is_correct") is True or (a.get("selected_answer") and a.get("selected_answer") == a.get("correct_answer"))
        )
    else:
        score = 0
        total = 1

    mastery_score = round((score / total) * 100.0, 1)

    if mastery_score >= 85.0:
        mastery_level = "Mastered"
        status = "MASTERED"
    elif mastery_score >= 60.0:
        mastery_level = "Competent"
        status = "COMPLETED"
    else:
        mastery_level = "Needs Practice"
        status = "COMPLETED"

    # Fetch or create progress record
    prog = db.query(TopicProgress).filter(
        TopicProgress.user_id == current_user.id,
        TopicProgress.topic_id == topic.id
    ).first()

    now = datetime.now(timezone.utc)
    if not prog:
        prog = TopicProgress(
            user_id=current_user.id,
            topic_id=topic.id,
            status=status,
            mastery_score=mastery_score,
            accuracy=mastery_score,
            recent_accuracy=mastery_score,
            attempts_count=total,
            correct_count=score,
            completed_steps=12,
            total_steps=12,
            last_practiced_at=now
        )
        db.add(prog)
    else:
        # Never downgrade MASTERED to COMPLETED
        if prog.status != "MASTERED":
            prog.status = status
        prog.mastery_score = max(prog.mastery_score, mastery_score)
        prog.completed_steps = prog.total_steps or 12
        prog.attempts_count += total
        prog.correct_count += score
        prog.last_practiced_at = now
        if prog.attempts_count > 0:
            prog.accuracy = round((prog.correct_count / prog.attempts_count) * 100.0, 1)
        prog.recent_accuracy = mastery_score

    # Record individual question attempts if answers provided
    if payload.answers:
        for a in payload.answers:
            qid = a.get("question_id")
            if qid:
                sel = str(a.get("selected_answer") or "")
                cor = bool(a.get("is_correct", False))
                sec = int(a.get("time_taken_seconds") or 0)
                attempt = UserQuestionAttempt(
                    user_id=current_user.id,
                    question_id=qid,
                    topic_id=topic.id,
                    selected_answer=sel,
                    is_correct=cor,
                    time_taken_seconds=sec,
                    created_at=now
                )
                db.add(attempt)

    # XP Award: 50 base + 5 per correct answer + 25 bonus if mastered
    xp_earned = 50 + (score * 5)
    if mastery_score >= 85.0:
        xp_earned += 25

    old_xp = current_user.xp or 0
    new_xp = old_xp + xp_earned
    old_level = current_user.level or 1
    new_level = (new_xp // 250) + 1
    level_up = new_level > old_level

    current_user.xp = new_xp
    current_user.level = new_level

    # Record XP transaction
    xp_tx = XPTransaction(
        user_id=current_user.id,
        amount=xp_earned,
        reason=f"Topic Quiz: {topic.title}",
        created_at=now
    )
    db.add(xp_tx)

    # Check and unlock next topic in the same subject
    next_topic = db.query(Topic).filter(
        Topic.subject_id == topic.subject_id,
        Topic.order == topic.order + 1
    ).first()

    unlocked_next = False
    next_slug = None
    next_title = None

    if next_topic:
        next_slug = next_topic.slug
        next_title = next_topic.title
        next_prog = db.query(TopicProgress).filter(
            TopicProgress.user_id == current_user.id,
            TopicProgress.topic_id == next_topic.id
        ).first()

        if not next_prog:
            next_prog = TopicProgress(
                user_id=current_user.id,
                topic_id=next_topic.id,
                status="AVAILABLE",
                mastery_score=0.0,
                accuracy=0.0,
                recent_accuracy=0.0,
                attempts_count=0,
                correct_count=0,
                completed_steps=0,
                total_steps=12,
                last_practiced_at=now
            )
            db.add(next_prog)
            unlocked_next = True
        elif next_prog.status == "LOCKED" or next_prog.status == "UPCOMING":
            next_prog.status = "AVAILABLE"
            unlocked_next = True

    db.commit()

    return QuizCompleteResponse(
        topic_id=topic.id,
        topic_slug=topic.slug,
        status=prog.status,
        mastery_score=mastery_score,
        mastery_level=mastery_level,
        xp_earned=xp_earned,
        xp_awarded=xp_earned,
        new_xp=new_xp,
        new_level=new_level,
        level_up=level_up,
        next_topic_slug=next_slug,
        next_topic_title=next_title,
        unlocked_next=unlocked_next
    )
