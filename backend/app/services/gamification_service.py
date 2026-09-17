import math
from datetime import datetime, date, timezone, timedelta
from typing import Tuple, List
from sqlalchemy.orm import Session
from app.models.user import User, LearningStreak, XPTransaction
from app.models.gamification import Achievement, UserAchievement, DailyQuest, UserDailyQuest
from app.models.learning import TopicProgress, UserQuestionAttempt

def calculate_level_from_xp(xp: int) -> int:
    """
    Calculates user level based on XP.
    Tuned so 2450 XP = Level 12.
    """
    if xp <= 0:
        return 1
    # Smooth progression matching Level 12 at 2,450 XP
    level = int(1 + (xp / 220.0))
    return max(1, level)

def award_xp(db: Session, user: User, amount: int, reason: str) -> Tuple[int, int, bool]:
    """
    Awards XP to the user, records transaction, and checks for level up.
    Returns: (new_xp, new_level, level_up_boolean)
    """
    old_level = user.level
    user.xp += amount
    new_level = calculate_level_from_xp(user.xp)
    level_up = new_level > old_level
    user.level = new_level

    # Log XP Transaction
    tx = XPTransaction(user_id=user.id, amount=amount, reason=reason)
    db.add(tx)

    # Check daily quests related to XP
    update_daily_quest_progress(db, user.id, "xp", amount)

    # Check XP achievements
    if user.xp >= 100:
        unlock_achievement(db, user.id, "xp_100")
    if user.xp >= 1000:
        unlock_achievement(db, user.id, "xp_1000")
    if user.xp >= 2500:
        unlock_achievement(db, user.id, "xp_2500")

    db.commit()
    db.refresh(user)
    return user.xp, user.level, level_up

def update_user_streak(db: Session, user_id: int) -> int:
    """Updates learning streak daily. Consecutive days increase streak."""
    today = datetime.now(timezone.utc).date()
    streak = db.query(LearningStreak).filter(LearningStreak.user_id == user_id).first()

    if not streak:
        streak = LearningStreak(
            user_id=user_id,
            current_streak=1,
            longest_streak=1,
            last_activity_date=today,
            weekly_history="M,T,W,T,F,S,S"
        )
        db.add(streak)
        db.commit()
        db.refresh(streak)
        return streak.current_streak

    if streak.last_activity_date is None:
        streak.current_streak = 1
        streak.longest_streak = max(streak.longest_streak, 1)
        streak.last_activity_date = today
    elif streak.last_activity_date == today:
        # Already practiced today
        pass
    elif streak.last_activity_date == today - timedelta(days=1):
        # Practiced yesterday, consecutive day
        streak.current_streak += 1
        streak.longest_streak = max(streak.longest_streak, streak.current_streak)
        streak.last_activity_date = today
    else:
        # Missed a day or more
        if streak.freeze_count > 0 and streak.last_activity_date == today - timedelta(days=2):
            # Used streak freeze forgiveness
            streak.freeze_count -= 1
            streak.current_streak += 1
            streak.last_activity_date = today
        else:
            streak.current_streak = 1
            streak.last_activity_date = today

    # Check streak achievements
    if streak.current_streak >= 7:
        unlock_achievement(db, user_id, "streak_7")
    if streak.current_streak >= 30:
        unlock_achievement(db, user_id, "streak_30")

    db.commit()
    return streak.current_streak

def unlock_achievement(db: Session, user_id: int, achievement_code: str) -> bool:
    """Unlocks an achievement if not already unlocked, and awards bonus XP."""
    ach = db.query(Achievement).filter(Achievement.code == achievement_code).first()
    if not ach:
        return False

    existing = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id,
        UserAchievement.achievement_id == ach.id
    ).first()

    if existing:
        return False

    user_ach = UserAchievement(user_id=user_id, achievement_id=ach.id)
    db.add(user_ach)

    # Award achievement XP
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.xp += ach.xp_reward
        user.level = calculate_level_from_xp(user.xp)
        tx = XPTransaction(user_id=user.id, amount=ach.xp_reward, reason=f"Unlocked {ach.title} Badge")
        db.add(tx)

    db.commit()
    return True

def update_daily_quest_progress(db: Session, user_id: int, quest_type: str, increment_by: int = 1):
    """Increments matching daily quest progress for today."""
    today = datetime.now(timezone.utc).date()
    user_quests = db.query(UserDailyQuest).join(DailyQuest).filter(
        UserDailyQuest.user_id == user_id,
        UserDailyQuest.quest_date == today,
        DailyQuest.quest_type == quest_type
    ).all()

    for uq in user_quests:
        if not uq.is_completed:
            uq.current_count += increment_by
            if uq.current_count >= uq.quest.target_count:
                uq.is_completed = True
                # Award quest XP
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    user.xp += uq.quest.xp_reward
                    user.level = calculate_level_from_xp(user.xp)
                    tx = XPTransaction(user_id=user.id, amount=uq.quest.xp_reward, reason=f"Completed Quest: {uq.quest.title}")
                    db.add(tx)
    db.commit()
