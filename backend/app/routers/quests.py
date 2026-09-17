from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.gamification import DailyQuest, UserDailyQuest
from app.schemas.gamification import DailyQuestResponse
from app.auth.deps import get_current_user

router = APIRouter(prefix="/quests", tags=["Daily Quests"])

@router.get("/today", response_model=List[DailyQuestResponse])
def get_today_quests(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = datetime.now(timezone.utc).date()
    
    # Ensure system daily quests exist
    all_quests = db.query(DailyQuest).all()
    if not all_quests:
        default_quests = [
            DailyQuest(title="Complete 3 lessons", quest_type="lessons", target_count=3, xp_reward=30),
            DailyQuest(title="Answer 10 questions", quest_type="questions", target_count=10, xp_reward=40),
            DailyQuest(title="Review 1 weak concept", quest_type="review", target_count=1, xp_reward=30),
            DailyQuest(title="Earn 100 XP today", quest_type="xp", target_count=100, xp_reward=50),
        ]
        db.add_all(default_quests)
        db.commit()
        all_quests = db.query(DailyQuest).all()

    # Ensure user has quest records for today
    user_quests = db.query(UserDailyQuest).filter(
        UserDailyQuest.user_id == current_user.id,
        UserDailyQuest.quest_date == today
    ).all()

    existing_quest_ids = {uq.quest_id for uq in user_quests}
    for q in all_quests:
        if q.id not in existing_quest_ids:
            new_uq = UserDailyQuest(
                user_id=current_user.id,
                quest_id=q.id,
                current_count=0,
                is_completed=False,
                quest_date=today
            )
            db.add(new_uq)
    db.commit()

    # Re-query
    user_quests = db.query(UserDailyQuest).filter(
        UserDailyQuest.user_id == current_user.id,
        UserDailyQuest.quest_date == today
    ).all()

    responses = []
    for uq in user_quests:
        responses.append(DailyQuestResponse(
            id=uq.quest.id,
            title=uq.quest.title,
            quest_type=uq.quest.quest_type,
            target_count=uq.quest.target_count,
            current_count=min(uq.quest.target_count, uq.current_count),
            is_completed=uq.is_completed,
            xp_reward=uq.quest.xp_reward
        ))

    return responses
