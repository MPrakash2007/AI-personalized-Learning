from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(50), default="🏆")
    category = Column(String(50), default="general")
    xp_reward = Column(Integer, default=50)

    user_achievements = relationship("UserAchievement", back_populates="achievement", cascade="all, delete-orphan")

class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False)
    unlocked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")

class DailyQuest(Base):
    __tablename__ = "daily_quests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    quest_type = Column(String(50), nullable=False)  # lessons, questions, review, xp
    target_count = Column(Integer, default=1)
    xp_reward = Column(Integer, default=30)

    user_quests = relationship("UserDailyQuest", back_populates="quest", cascade="all, delete-orphan")

class UserDailyQuest(Base):
    __tablename__ = "user_daily_quests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quest_id = Column(Integer, ForeignKey("daily_quests.id", ondelete="CASCADE"), nullable=False)
    current_count = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    quest_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="daily_quests")
    quest = relationship("DailyQuest", back_populates="user_quests")

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    challenge_type = Column(String(50), default="daily")  # daily, weekly, monthly, boss
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True)
    description = Column(Text, nullable=False)
    duration_minutes = Column(Integer, default=15)
    xp_reward = Column(Integer, default=100)
    questions_count = Column(Integer, default=5)

    attempts = relationship("ChallengeAttempt", back_populates="challenge", cascade="all, delete-orphan")

class ChallengeAttempt(Base):
    __tablename__ = "challenge_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)
    time_spent_seconds = Column(Integer, default=0)
    completed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="challenge_attempts")
    challenge = relationship("Challenge", back_populates="attempts")
