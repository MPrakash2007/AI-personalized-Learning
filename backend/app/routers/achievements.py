from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.gamification import Achievement, UserAchievement
from app.schemas.gamification import AchievementResponse
from app.auth.deps import get_current_user

router = APIRouter(prefix="/achievements", tags=["Achievements"])

@router.get("", response_model=List[AchievementResponse])
def get_all_achievements(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    achievements = db.query(Achievement).all()
    user_achievements = db.query(UserAchievement).filter(UserAchievement.user_id == current_user.id).all()
    unlocked_map = {ua.achievement_id: ua.unlocked_at for ua in user_achievements}

    results = []
    for ach in achievements:
        is_unlocked = ach.id in unlocked_map
        results.append(AchievementResponse(
            id=ach.id,
            code=ach.code,
            title=ach.title,
            description=ach.description,
            icon=ach.icon,
            category=ach.category,
            xp_reward=ach.xp_reward,
            is_unlocked=is_unlocked,
            unlocked_at=unlocked_map.get(ach.id)
        ))

    return results
