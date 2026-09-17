from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.learning import Lesson, LessonStep, TopicProgress, Topic
from app.models.user import User
from app.schemas.learning import LessonResponse
from app.auth.deps import get_current_user
from app.services.gamification_service import award_xp, update_user_streak, update_daily_quest_progress

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.get("/{id}", response_model=LessonResponse)
def get_lesson(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = db.query(Lesson).filter(Lesson.id == id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.post("/{id}/complete")
def complete_lesson(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = db.query(Lesson).filter(Lesson.id == id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Update streak
    update_user_streak(db, current_user.id)

    # Award XP (+20 XP for lesson completion, or lesson.xp_reward)
    xp_to_award = lesson.xp_reward or 20
    new_xp, new_level, level_up = award_xp(
        db, current_user, xp_to_award, f"Completed lesson: {lesson.title}"
    )

    # Update daily quests
    update_daily_quest_progress(db, current_user.id, "lessons", 1)

    # Update topic progress steps
    prog = db.query(TopicProgress).filter(
        TopicProgress.user_id == current_user.id,
        TopicProgress.topic_id == lesson.topic_id
    ).first()

    if prog:
        prog.completed_steps = min(prog.total_steps, prog.completed_steps + 1)
        if prog.status == "LOCKED":
            prog.status = "IN_PROGRESS"
        db.commit()

    return {
        "success": True,
        "xp_earned": xp_to_award,
        "new_xp": new_xp,
        "new_level": new_level,
        "level_up": level_up,
        "message": f"Congratulations! You completed '{lesson.title}'."
    }
