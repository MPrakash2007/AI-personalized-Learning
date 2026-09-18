"""
CodeOrbit Practice Router
Handles dedicated practice questions endpoint with subject isolation,
completed-topics enforcement, randomization, and session management.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from app.database import get_db
from app.models.user import User
from app.models.learning import (
    Question, Topic, Subject, PracticeSession, PracticeSessionQuestion,
    TopicProgress, UserQuestionAttempt
)
from app.schemas.learning import QuestionResponse
from app.auth.deps import get_current_user
from app.services.practice_service import get_practice_questions, create_practice_session
from app.services.gamification_service import award_xp, update_user_streak, update_daily_quest_progress
from app.services.progress_service import calculate_mastery_score

router = APIRouter(prefix="/practice", tags=["Practice Arena"])

@router.get("/questions")
def query_practice_questions(
    subject_id: Optional[int] = None,
    subject_slug: Optional[str] = None,
    difficulty: Optional[str] = None,
    mode: str = "quick",
    limit: Optional[int] = Query(None, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns randomized PRACTICE questions adhering to:
    1. Only topics within subject_id / subject_slug.
    2. Only topics the student has completed/mastered.
    3. question_context == 'PRACTICE'.
    4. Helpful empty state guidance if no topics completed yet.
    """
    if not subject_id and subject_slug:
        subj = db.query(Subject).filter(Subject.slug == subject_slug).first()
        if subj:
            subject_id = subj.id

    result = get_practice_questions(
        db=db,
        current_user=current_user,
        subject_id=subject_id,
        difficulty=difficulty,
        mode=mode,
        limit=limit
    )

    formatted_questions = [
        QuestionResponse.model_validate(q) for q in result["questions"]
    ]

    completed_topic_ids = result.get("completed_topic_ids", [])
    completed_topics_objs = []
    if completed_topic_ids:
        topics_db = db.query(Topic).filter(Topic.id.in_(completed_topic_ids)).all()
        completed_topics_objs = [{"id": t.id, "title": t.title, "slug": t.slug} for t in topics_db]

    return {
        "success": True,
        "can_practice": result["can_practice"],
        "message": result["message"],
        "subject_name": result["subject_name"],
        "completed_topics_count": result["completed_topics_count"],
        "completed_topics": completed_topics_objs,
        "questions": formatted_questions
    }

@router.post("/sessions")
def start_practice_session(
    subject_id: Optional[int] = None,
    mode: str = "quick",
    difficulty: Optional[str] = None,
    limit: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start a tracked practice session."""
    session = create_practice_session(
        db=db,
        current_user=current_user,
        subject_id=subject_id,
        mode=mode,
        difficulty=difficulty,
        limit=limit
    )
    return {
        "session_id": session.id,
        "total_questions": session.total_questions,
        "mode": session.mode,
        "started_at": session.started_at
    }

@router.get("/sessions/{session_id}")
def get_practice_session_details(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(PracticeSession).filter(
        PracticeSession.id == session_id,
        PracticeSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Practice session not found")

    questions_data = []
    for sq in session.session_questions:
        q = sq.question
        if q:
            questions_data.append({
                "order_number": sq.order_number,
                "question": QuestionResponse.model_validate(q),
                "user_answer": sq.user_answer,
                "is_correct": sq.is_correct
            })

    return {
        "id": session.id,
        "mode": session.mode,
        "subject_id": session.subject_id,
        "score": session.score,
        "total_questions": session.total_questions,
        "started_at": session.started_at,
        "ended_at": session.ended_at,
        "questions": questions_data
    }

@router.post("/sessions/{session_id}/complete")
def complete_practice_session(
    session_id: int,
    results: Dict[str, Any],  # { "answers": [{"question_id": int, "selected_answer": str, "is_correct": bool}] }
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(PracticeSession).filter(
        PracticeSession.id == session_id,
        PracticeSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Practice session not found")

    answers = results.get("answers", [])
    correct_count = sum(1 for a in answers if a.get("is_correct"))
    total_answered = len(answers)
    accuracy = round((correct_count / max(1, total_answered)) * 100, 1)

    session.score = correct_count
    session.total_questions = total_answered
    session.ended_at = datetime.now(timezone.utc)

    # Award practice XP: 5 XP per correct answer + 20 XP bonus for completing session
    xp_earned = (correct_count * 5) + 20
    new_xp, new_level, level_up = award_xp(db, current_user, xp_earned, f"Practice Arena Session ({correct_count}/{total_answered})")
    update_user_streak(db, current_user.id)
    update_daily_quest_progress(db, current_user.id, "questions", total_answered)

    # Identify strong vs weak topics
    topic_performance = {}
    for a in answers:
        q = db.query(Question).filter(Question.id == a.get("question_id")).first()
        if q:
            t_title = q.topic.title if q.topic else "General"
            if t_title not in topic_performance:
                topic_performance[t_title] = {"correct": 0, "total": 0}
            topic_performance[t_title]["total"] += 1
            if a.get("is_correct"):
                topic_performance[t_title]["correct"] += 1

    strong_topics = [t for t, p in topic_performance.items() if (p["correct"] / p["total"]) >= 0.7]
    needs_practice = [t for t, p in topic_performance.items() if (p["correct"] / p["total"]) < 0.7]

    db.commit()

    return {
        "success": True,
        "score": correct_count,
        "total_questions": total_answered,
        "accuracy": accuracy,
        "xp_earned": xp_earned,
        "new_xp": new_xp,
        "new_level": new_level,
        "level_up": level_up,
        "strong_topics": strong_topics,
        "needs_practice": needs_practice
    }
