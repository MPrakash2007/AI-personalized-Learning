from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.learning import TopicProgress, Topic, Subject, Question, UserQuestionAttempt

def calculate_next_review_date(accuracy: float, recent_mistakes_count: int) -> datetime:
    """
    Computes spaced repetition interval based on accuracy and recent mistakes:
    < 50%  -> 1 day
    50-70% -> 3 days
    70-85% -> 7 days
    85%+   -> 14 days
    If recent mistakes exist, deduct 1 day (minimum 1 day).
    """
    now = datetime.now(timezone.utc)
    if accuracy < 50.0:
        days = 1
    elif accuracy < 70.0:
        days = 3
    elif accuracy < 85.0:
        days = 7
    else:
        days = 14

    if recent_mistakes_count > 2:
        days = max(1, days - 2)
    elif recent_mistakes_count > 0:
        days = max(1, days - 1)

    return now + timedelta(days=days)

def get_due_for_review_topics(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """Returns topics that are due for smart review."""
    now = datetime.now(timezone.utc)
    
    # Progress records where next_review_due <= now or last_practiced_at is stale
    progress_list = db.query(TopicProgress).filter(
        TopicProgress.user_id == user_id,
        TopicProgress.attempts_count > 0
    ).all()

    due_topics = []
    for p in progress_list:
        topic = db.query(Topic).filter(Topic.id == p.topic_id).first()
        if not topic:
            continue
        subject = db.query(Subject).filter(Subject.id == topic.subject_id).first()

        # Calculate days since last practiced
        days_since = 0
        if p.last_practiced_at:
            delta = now - p.last_practiced_at.replace(tzinfo=timezone.utc) if p.last_practiced_at.tzinfo is None else now - p.last_practiced_at
            days_since = max(1, delta.days)

        is_due = False
        if p.next_review_due and p.next_review_due.replace(tzinfo=timezone.utc) <= now:
            is_due = True
        elif p.accuracy < 60.0 and days_since >= 1:
            is_due = True
        elif p.accuracy < 80.0 and days_since >= 3:
            is_due = True
        elif days_since >= 7:
            is_due = True

        if is_due:
            # Fetch sample review questions
            questions = db.query(Question).filter(Question.topic_id == topic.id).limit(5).all()
            due_topics.append({
                "topic_id": topic.id,
                "topic_title": topic.title,
                "topic_slug": topic.slug,
                "subject_id": subject.id if subject else 0,
                "subject_name": subject.name if subject else "General",
                "subject_slug": subject.slug if subject else "general",
                "subject_icon": subject.icon if subject else "📚",
                "accuracy": p.accuracy,
                "mastery": p.mastery_score,
                "days_since_practiced": days_since,
                "questions_count": len(questions)
            })

    return due_topics
