from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.learning import Subject, Topic, TopicProgress
from app.models.user import User
from app.schemas.learning import SubjectResponse, SubjectDetailResponse, TopicResponse, TopicProgressResponse
from app.auth.deps import get_current_user

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.get("", response_model=List[SubjectResponse])
def get_all_subjects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subjects = db.query(Subject).order_by(Subject.order.asc()).all()
    results = []

    for s in subjects:
        topics = db.query(Topic).filter(Topic.subject_id == s.id).all()
        total_topics = len(topics)
        topic_ids = [t.id for t in topics]

        progress_records = db.query(TopicProgress).filter(
            TopicProgress.user_id == current_user.id,
            TopicProgress.topic_id.in_(topic_ids)
        ).all() if topic_ids else []

        completed_count = sum(1 for p in progress_records if p.status in ["COMPLETED", "MASTERED"])
        progress_pct = (completed_count / total_topics * 100.0) if total_topics > 0 else 0.0

        total_mastery = sum(p.mastery_score for p in progress_records)
        avg_mastery = (total_mastery / total_topics) if total_topics > 0 else 0.0

        results.append(SubjectResponse(
            id=s.id,
            name=s.name,
            slug=s.slug,
            icon=s.icon,
            description=s.description,
            color=s.color,
            order=s.order,
            topics_count=total_topics,
            completed_topics_count=completed_count,
            progress_percentage=round(progress_pct, 1),
            overall_mastery=round(avg_mastery, 1)
        ))

    return results

@router.get("/{slug_or_id}", response_model=SubjectDetailResponse)
def get_subject_detail(slug_or_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if slug_or_id.isdigit():
        subject = db.query(Subject).filter(Subject.id == int(slug_or_id)).first()
    else:
        subject = db.query(Subject).filter(Subject.slug == slug_or_id.lower()).first()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    topics = db.query(Topic).filter(Topic.subject_id == subject.id).order_by(Topic.order.asc()).all()
    total_topics = len(topics)
    topic_responses = []
    completed_count = 0
    total_mastery = 0.0

    # Load all user progress for this subject's topics in one query
    topic_ids = [t.id for t in topics]
    user_progress_map = {}
    if topic_ids:
        progress_records = db.query(TopicProgress).filter(
            TopicProgress.user_id == current_user.id,
            TopicProgress.topic_id.in_(topic_ids)
        ).all()
        user_progress_map = {p.topic_id: p for p in progress_records}

    current_assigned = False
    next_assigned = False

    for idx, t in enumerate(topics):
        prog = user_progress_map.get(t.id)
        is_completed = bool(prog and prog.status in ["COMPLETED", "MASTERED"])
        
        if is_completed:
            completed_count += 1
            total_mastery += prog.mastery_score

        # Sequential Accessibility Rule:
        # Topic 1 is ALWAYS accessible.
        # Topic N (N > 1) is accessible iff Topic N-1 is COMPLETED or MASTERED.
        # Completed topics remain permanently accessible (COMPLETED != LOCKED).
        if idx == 0:
            is_accessible = True
        else:
            prev_topic = topics[idx - 1]
            prev_prog = user_progress_map.get(prev_topic.id)
            prev_completed = bool(prev_prog and prev_prog.status in ["COMPLETED", "MASTERED"])
            is_accessible = prev_completed

        # Determine status
        if is_completed:
            status = prog.status if (prog and prog.status) else "COMPLETED"
        elif is_accessible:
            status = "AVAILABLE"
        else:
            status = "UPCOMING"

        # Determine current active topic and next upcoming topic
        is_current = False
        is_next = False
        if is_accessible and not is_completed and not current_assigned:
            is_current = True
            current_assigned = True
        elif not is_accessible and not next_assigned:
            is_next = True
            next_assigned = True

        if prog:
            prog_data = TopicProgressResponse(
                topic_id=t.id,
                status=status,
                mastery_score=prog.mastery_score,
                accuracy=prog.accuracy,
                recent_accuracy=prog.recent_accuracy,
                attempts_count=prog.attempts_count,
                correct_count=prog.correct_count,
                completed_steps=prog.completed_steps,
                total_steps=prog.total_steps,
                last_practiced_at=prog.last_practiced_at,
                next_review_due=prog.next_review_due,
                is_accessible=is_accessible,
                is_completed=is_completed,
                is_current=is_current,
                is_next=is_next
            )
        else:
            prog_data = TopicProgressResponse(
                topic_id=t.id,
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
                is_current=is_current,
                is_next=is_next
            )

        topic_responses.append(TopicResponse(
            id=t.id,
            subject_id=t.subject_id,
            title=t.title,
            slug=t.slug,
            description=t.description,
            order=t.order,
            is_boss=t.is_boss,
            boss_title=t.boss_title,
            lessons_count=len(t.lessons),
            questions_count=len(t.questions),
            is_accessible=is_accessible,
            is_completed=is_completed,
            status=status,
            progress=prog_data
        ))

    progress_pct = (completed_count / total_topics * 100.0) if total_topics > 0 else 0.0
    avg_mastery = (total_mastery / total_topics) if total_topics > 0 else 0.0

    return SubjectDetailResponse(
        id=subject.id,
        name=subject.name,
        slug=subject.slug,
        icon=subject.icon,
        description=subject.description,
        color=subject.color,
        order=subject.order,
        topics_count=total_topics,
        completed_topics_count=completed_count,
        progress_percentage=round(progress_pct, 1),
        overall_mastery=round(avg_mastery, 1),
        topics=topic_responses
    )
