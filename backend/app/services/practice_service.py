"""
CodeOrbit Practice Service
Enforces strict subject boundaries, completed/mastered topic filtering,
PRACTICE question context isolation, randomized selection, and session tracking.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.learning import (
    Question, Topic, Subject, TopicProgress, UserQuestionAttempt,
    PracticeSession, PracticeSessionQuestion
)
from app.models.user import User

COMPLETED_STATUSES = ["COMPLETED", "MASTERED"]

def get_completed_topic_ids_for_user(
    db: Session,
    user_id: int,
    subject_id: Optional[int] = None
) -> List[int]:
    """Retrieve list of topic IDs that user has completed or mastered, optionally restricted by subject."""
    query = db.query(TopicProgress.topic_id).join(Topic, Topic.id == TopicProgress.topic_id)
    query = query.filter(
        TopicProgress.user_id == user_id,
        TopicProgress.status.in_(COMPLETED_STATUSES)
    )
    if subject_id:
        query = query.filter(Topic.subject_id == subject_id)
    
    return [row[0] for row in query.all()]

def get_practice_questions(
    db: Session,
    current_user: User,
    subject_id: Optional[int] = None,
    difficulty: Optional[str] = None,
    mode: str = "quick",
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Select practice questions adhering strictly to:
    1. subject_id constraint (never leak other subjects).
    2. completed topics only (TopicProgress.status in ['COMPLETED', 'MASTERED']).
    3. question_context == 'PRACTICE' (distinct from LEARN questions).
    4. randomized ordering.
    5. avoid recently answered questions.
    """
    # Determine limit based on mode
    if limit is None:
        if mode == "quick":
            limit = 10
        elif mode == "timed":
            limit = 20
        elif mode == "weak":
            limit = 10
        else:
            limit = 15

    # 1. Fetch completed topic IDs
    completed_topic_ids = get_completed_topic_ids_for_user(db, current_user.id, subject_id)

    # Subject lookup for friendly message
    subject_name = "curriculum"
    if subject_id:
        subj = db.query(Subject).filter(Subject.id == subject_id).first()
        if subj:
            subject_name = subj.name

    # 2. If no completed topics, return empty state with educational guidance
    if not completed_topic_ids:
        return {
            "questions": [],
            "completed_topics_count": 0,
            "subject_name": subject_name,
            "can_practice": False,
            "message": f"📚 Complete a {subject_name} lesson first. You need to finish at least one {subject_name} topic before starting subject-specific practice."
        }

    # 3. Base Query on Questions
    query = db.query(Question).filter(
        Question.topic_id.in_(completed_topic_ids),
        Question.question_context == "PRACTICE"
    )

    # If subject_id is specified, ensure double-check on topic's subject_id
    if subject_id:
        query = query.join(Topic, Topic.id == Question.topic_id).filter(Topic.subject_id == subject_id)

    if difficulty and difficulty.upper() in ["EASY", "MEDIUM", "HARD"]:
        query = query.filter(Question.difficulty == difficulty.upper())

    # Mode-specific filters
    if mode == "weak":
        # Find topics where mastery < 60% or recent accuracy < 60%
        weak_topic_ids = [
            row[0] for row in db.query(TopicProgress.topic_id).filter(
                TopicProgress.user_id == current_user.id,
                TopicProgress.topic_id.in_(completed_topic_ids),
                (TopicProgress.mastery_score < 60.0) | (TopicProgress.recent_accuracy < 60.0)
            ).all()
        ]
        if weak_topic_ids:
            query = query.filter(Question.topic_id.in_(weak_topic_ids))

    # 4. Exclude recently answered questions to prevent rapid repetition
    recent_q_ids = [
        row[0] for row in db.query(UserQuestionAttempt.question_id).filter(
            UserQuestionAttempt.user_id == current_user.id
        ).order_by(UserQuestionAttempt.created_at.desc()).limit(15).all()
    ]

    all_matched = query.all()
    
    # Try filtering out recent questions
    non_recent = [q for q in all_matched if q.id not in recent_q_ids]
    candidate_pool = non_recent if len(non_recent) >= limit else all_matched

    # 5. Randomized selection
    # Using python random shuffle to be database-agnostic and avoid ordering bugs
    import random
    random.shuffle(candidate_pool)
    selected_questions = candidate_pool[:limit]

    return {
        "questions": selected_questions,
        "completed_topics_count": len(completed_topic_ids),
        "completed_topic_ids": completed_topic_ids,
        "subject_name": subject_name,
        "can_practice": True,
        "message": f"Loaded {len(selected_questions)} practice questions from your completed {subject_name} topics."
    }

def create_practice_session(
    db: Session,
    current_user: User,
    subject_id: Optional[int] = None,
    mode: str = "quick",
    difficulty: Optional[str] = None,
    limit: Optional[int] = None
) -> PracticeSession:
    """Create a tracked practice session with stored question sequence."""
    result = get_practice_questions(db, current_user, subject_id, difficulty, mode, limit)
    questions = result["questions"]

    session = PracticeSession(
        user_id=current_user.id,
        subject_id=subject_id,
        mode=mode,
        total_questions=len(questions),
        score=0,
        started_at=datetime.now(timezone.utc)
    )
    db.add(session)
    db.flush()

    for idx, q in enumerate(questions, start=1):
        sq = PracticeSessionQuestion(
            session_id=session.id,
            question_id=q.id,
            order_number=idx
        )
        db.add(sq)

    db.commit()
    db.refresh(session)
    return session
