from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone
from app.models.learning import TopicProgress, UserQuestionAttempt, Topic, Question, Lesson
from app.models.user import User

def calculate_mastery_score(accuracy: float, recent_accuracy: float, completion_ratio: float) -> float:
    """
    Calculates topic mastery based on the formula:
    mastery = (accuracy * 0.5) + (recent_accuracy * 0.3) + (completion_ratio * 100 * 0.2)
    Clamped strictly between 0.0 and 100.0.
    """
    raw_mastery = (accuracy * 0.5) + (recent_accuracy * 0.3) + (completion_ratio * 100.0 * 0.2)
    return round(max(0.0, min(100.0, raw_mastery)), 1)

def get_mastery_level_title(score: float) -> str:
    if score >= 86.0:
        return "Mastered"
    elif score >= 71.0:
        return "Strong"
    elif score >= 51.0:
        return "Developing"
    elif score >= 31.0:
        return "Learning"
    else:
        return "Beginner"

def update_topic_progress_after_attempt(
    db: Session,
    user_id: int,
    topic_id: int,
    is_correct: bool
) -> TopicProgress:
    """Updates question attempt metrics, computes accuracy and mastery, and unlocks next milestones."""
    progress = db.query(TopicProgress).filter(
        TopicProgress.user_id == user_id,
        TopicProgress.topic_id == topic_id
    ).first()

    if not progress:
        progress = TopicProgress(
            user_id=user_id,
            topic_id=topic_id,
            status="IN_PROGRESS",
            completed_steps=1,
            total_steps=6,
            attempts_count=0,
            correct_count=0
        )
        db.add(progress)
        db.flush()

    # Query all attempts for this user & topic
    attempts = db.query(UserQuestionAttempt).filter(
        UserQuestionAttempt.user_id == user_id,
        UserQuestionAttempt.topic_id == topic_id
    ).order_by(UserQuestionAttempt.created_at.desc()).all()

    total_attempts = len(attempts)
    correct_attempts = sum(1 for a in attempts if a.is_correct)
    accuracy = (correct_attempts / total_attempts * 100.0) if total_attempts > 0 else 0.0

    # Recent accuracy (last 5 attempts)
    recent_attempts = attempts[:5]
    recent_correct = sum(1 for a in recent_attempts if a.is_correct)
    recent_accuracy = (recent_correct / len(recent_attempts) * 100.0) if recent_attempts else accuracy

    completion_ratio = min(1.0, max(0.2, progress.completed_steps / max(1, progress.total_steps)))

    old_mastery = progress.mastery_score
    new_mastery = calculate_mastery_score(accuracy, recent_accuracy, completion_ratio)

    progress.attempts_count = total_attempts
    progress.correct_count = correct_attempts
    progress.accuracy = round(accuracy, 1)
    progress.recent_accuracy = round(recent_accuracy, 1)
    progress.mastery_score = new_mastery
    progress.last_practiced_at = datetime.now(timezone.utc)

    # Determine status
    if new_mastery >= 85.0:
        progress.status = "MASTERED"
    elif new_mastery >= 50.0:
        progress.status = "COMPLETED"
    else:
        progress.status = "IN_PROGRESS"

    db.commit()
    db.refresh(progress)

    # If completed or mastered, automatically ensure next topic in sequence is AVAILABLE
    current_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if current_topic and (progress.status in ["COMPLETED", "MASTERED"]):
        next_topic = db.query(Topic).filter(
            Topic.subject_id == current_topic.subject_id,
            Topic.order > current_topic.order
        ).order_by(Topic.order.asc()).first()

        if next_topic:
            next_progress = db.query(TopicProgress).filter(
                TopicProgress.user_id == user_id,
                TopicProgress.topic_id == next_topic.id
            ).first()
            if not next_progress:
                next_progress = TopicProgress(
                    user_id=user_id,
                    topic_id=next_topic.id,
                    status="AVAILABLE",
                    completed_steps=0,
                    total_steps=6
                )
                db.add(next_progress)
                db.commit()
            elif next_progress.status == "LOCKED":
                next_progress.status = "AVAILABLE"
                db.commit()

    return progress
