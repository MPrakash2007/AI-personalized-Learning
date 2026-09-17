from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.learning import Subject, Topic, Lesson, Question, UserQuestionAttempt
from app.auth.deps import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin CMS"])

@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    total_users = db.query(User).count()
    total_subjects = db.query(Subject).count()
    total_topics = db.query(Topic).count()
    total_lessons = db.query(Lesson).count()
    total_questions = db.query(Question).count()
    total_attempts = db.query(UserQuestionAttempt).count()

    return {
        "total_users": total_users,
        "total_subjects": total_subjects,
        "total_topics": total_topics,
        "total_lessons": total_lessons,
        "total_questions": total_questions,
        "total_attempts": total_attempts
    }

@router.get("/users")
def get_all_users(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    users = db.query(User).order_by(User.created_at.desc()).limit(50).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "college": u.college,
            "level": u.level,
            "xp": u.xp,
            "is_admin": u.is_admin,
            "created_at": u.created_at
        }
        for u in users
    ]
