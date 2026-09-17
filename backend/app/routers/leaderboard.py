from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User, LearningStreak
from app.models.learning import TopicProgress
from app.schemas.gamification import LeaderboardResponse, LeaderboardUser
from app.auth.deps import get_current_user

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

@router.get("", response_model=LeaderboardResponse)
def get_leaderboard(
    timeframe: str = Query("weekly", regex="^(weekly|monthly|all_time)$"),
    category: str = Query("global", regex="^(global|college|friends)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(User)

    if category == "college" and current_user.college:
        query = query.filter(User.college == current_user.college)

    # Sort users by XP desc
    users = query.order_by(User.xp.desc()).limit(20).all()

    leaderboard_users = []
    for rank, u in enumerate(users, start=1):
        streak = db.query(LearningStreak).filter(LearningStreak.user_id == u.id).first()
        streak_val = streak.current_streak if streak else 0

        # Calculate average mastery
        progress_records = db.query(TopicProgress).filter(TopicProgress.user_id == u.id).all()
        avg_mastery = (sum(p.mastery_score for p in progress_records) / max(1, len(progress_records))) if progress_records else 0.0

        leaderboard_users.append(LeaderboardUser(
            rank=rank,
            user_id=u.id,
            full_name=u.full_name,
            college=u.college or "Tech University",
            avatar_url=u.avatar_url,
            level=u.level,
            xp=u.xp,
            streak=streak_val,
            mastery_score=round(avg_mastery, 1)
        ))

    return LeaderboardResponse(
        timeframe=timeframe,
        category=category,
        users=leaderboard_users
    )
