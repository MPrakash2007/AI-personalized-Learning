from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class AchievementResponse(BaseModel):
    id: int
    code: str
    title: str
    description: str
    icon: str
    category: str
    xp_reward: int
    is_unlocked: bool = False
    unlocked_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DailyQuestResponse(BaseModel):
    id: int
    title: str
    quest_type: str
    target_count: int
    current_count: int = 0
    is_completed: bool = False
    xp_reward: int

    class Config:
        from_attributes = True

class ChallengeResponse(BaseModel):
    id: int
    title: str
    challenge_type: str
    subject_id: Optional[int] = None
    description: str
    duration_minutes: int
    xp_reward: int
    questions_count: int
    is_completed: bool = False
    best_score: Optional[int] = None

    class Config:
        from_attributes = True

class ChallengeSubmitRequest(BaseModel):
    challenge_id: int
    score: int
    accuracy: float
    time_spent_seconds: int

class ChallengeSubmitResponse(BaseModel):
    xp_earned: int
    new_xp: int
    new_level: int
    message: str

class LeaderboardUser(BaseModel):
    rank: int
    user_id: int
    full_name: str
    college: Optional[str] = None
    avatar_url: Optional[str] = None
    level: int
    xp: int
    streak: int
    mastery_score: float

class LeaderboardResponse(BaseModel):
    timeframe: str  # weekly, monthly, all_time
    category: str   # global, college, friends
    users: List[LeaderboardUser]
