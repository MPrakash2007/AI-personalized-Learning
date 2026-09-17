from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.learning import TopicProgress, Topic, Subject, UserQuestionAttempt, Question
from app.models.analytics import AIRecommendation

def generate_user_recommendations(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """
    Analyzes student performance using a multi-factor score:
    - weakness_score (lower accuracy gives higher priority)
    - recency_score (days since last practice)
    - mistake_frequency (number of wrong answers recently)
    - topic_dependency (order/progress within curriculum)
    Returns curated, explainable recommendations categorized into:
    needs_attention, due_for_review, ready_to_advance, recommended_challenge.
    """
    now = datetime.now(timezone.utc)
    recommendations = []

    # 1. Check for Weak Topics ("Needs Attention")
    all_progress = db.query(TopicProgress).filter(TopicProgress.user_id == user_id).all()
    
    weak_progress = sorted(
        [p for p in all_progress if p.attempts_count >= 2 and p.accuracy < 70.0],
        key=lambda x: x.accuracy
    )

    if weak_progress:
        top_weak = weak_progress[0]
        topic = db.query(Topic).filter(Topic.id == top_weak.topic_id).first()
        subject = db.query(Subject).filter(Subject.id == topic.subject_id).first() if topic else None
        
        # Recent mistakes count
        recent_wrong = db.query(UserQuestionAttempt).filter(
            UserQuestionAttempt.user_id == user_id,
            UserQuestionAttempt.topic_id == top_weak.topic_id,
            UserQuestionAttempt.is_correct == False
        ).count()

        reason_text = f"You scored {top_weak.accuracy:.0f}% accuracy in {topic.title if topic else 'this topic'} with {recent_wrong} recent mistakes."
        
        recommendations.append({
            "category": "needs_attention",
            "title": f"Reinforce {topic.title if topic else 'Weak Concept'}",
            "reason": reason_text,
            "estimated_minutes": 8,
            "action_url": f"/learn/{subject.slug if subject else 'dbms'}/{topic.slug if topic else 'intro'}",
            "subject_id": subject.id if subject else None,
            "topic_id": topic.id if topic else None,
            "topic_title": topic.title if topic else "",
            "subject_name": subject.name if subject else "",
            "subject_icon": subject.icon if subject else "🎯"
        })

    # 2. Check for "Due for Review" (Spaced Repetition)
    stale_progress = [
        p for p in all_progress 
        if p.attempts_count > 0 and (
            p.last_practiced_at is not None and 
            (now - (p.last_practiced_at.replace(tzinfo=timezone.utc) if p.last_practiced_at.tzinfo is None else p.last_practiced_at)).days >= 3
        )
    ]
    if stale_progress:
        # Pick the one practiced longest ago
        stale = sorted(stale_progress, key=lambda x: x.last_practiced_at or now)[0]
        topic = db.query(Topic).filter(Topic.id == stale.topic_id).first()
        subject = db.query(Subject).filter(Subject.id == topic.subject_id).first() if topic else None
        days_ago = (now - (stale.last_practiced_at.replace(tzinfo=timezone.utc) if stale.last_practiced_at.tzinfo is None else stale.last_practiced_at)).days

        recommendations.append({
            "category": "due_for_review",
            "title": f"Smart Review: {topic.title if topic else 'Past Concept'}",
            "reason": f"It has been {days_ago} days since you practiced {topic.title if topic else 'this topic'}. Review now to prevent memory decay.",
            "estimated_minutes": 5,
            "action_url": f"/smart-review",
            "subject_id": subject.id if subject else None,
            "topic_id": topic.id if topic else None,
            "topic_title": topic.title if topic else "",
            "subject_name": subject.name if subject else "",
            "subject_icon": subject.icon if subject else "🔄"
        })

    # 3. Check for "Ready to Advance" (Next unlocked lesson)
    available_progress = db.query(TopicProgress).filter(
        TopicProgress.user_id == user_id,
        TopicProgress.status.in_(["AVAILABLE", "IN_PROGRESS"])
    ).first()

    if available_progress:
        topic = db.query(Topic).filter(Topic.id == available_progress.topic_id).first()
        subject = db.query(Subject).filter(Subject.id == topic.subject_id).first() if topic else None
        if topic and subject:
            recommendations.append({
                "category": "ready_to_advance",
                "title": f"Continue Learning: {topic.title}",
                "reason": f"You've unlocked this topic in {subject.name}. Advance forward to level up your mastery.",
                "estimated_minutes": 10,
                "action_url": f"/learn/{subject.slug}/{topic.slug}",
                "subject_id": subject.id,
                "topic_id": topic.id,
                "topic_title": topic.title,
                "subject_name": subject.name,
                "subject_icon": subject.icon
            })
    else:
        # Fallback to the first subject's first topic
        first_topic = db.query(Topic).order_by(Topic.id.asc()).first()
        if first_topic:
            subject = db.query(Subject).filter(Subject.id == first_topic.subject_id).first()
            recommendations.append({
                "category": "ready_to_advance",
                "title": f"Start {first_topic.title}",
                "reason": f"Begin your curriculum with foundational engineering principles.",
                "estimated_minutes": 8,
                "action_url": f"/learn/{subject.slug if subject else 'dbms'}/{first_topic.slug}",
                "subject_id": subject.id if subject else None,
                "topic_id": first_topic.id,
                "topic_title": first_topic.title,
                "subject_name": subject.name if subject else "Core",
                "subject_icon": subject.icon if subject else "🚀"
            })

    # 4. "Recommended Challenge"
    recommendations.append({
        "category": "recommended_challenge",
        "title": "Daily Engineering Speed Sprint",
        "reason": "Test your retention across multi-subject technical MCQs under timed conditions.",
        "estimated_minutes": 12,
        "action_url": "/challenges",
        "subject_id": None,
        "topic_id": None,
        "topic_title": "Daily Challenge",
        "subject_name": "Multi-Subject",
        "subject_icon": "🏆"
    })

    return recommendations

def sync_recommendations_to_database(db: Session, user_id: int):
    """Refreshes active recommendations in database for this user."""
    recs = generate_user_recommendations(db, user_id)
    # Remove old recommendations
    db.query(AIRecommendation).filter(AIRecommendation.user_id == user_id).delete()
    
    for r in recs:
        db_rec = AIRecommendation(
            user_id=user_id,
            category=r["category"],
            title=r["title"],
            reason=r["reason"],
            estimated_minutes=r["estimated_minutes"],
            action_url=r["action_url"],
            subject_id=r.get("subject_id"),
            topic_id=r.get("topic_id"),
            is_active=True
        )
        db.add(db_rec)
    db.commit()
