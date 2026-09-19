from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    college = Column(String(255), nullable=True)
    degree = Column(String(100), nullable=True)
    branch = Column(String(100), nullable=True)
    graduation_year = Column(Integer, nullable=True)
    avatar_url = Column(String(500), default="https://api.dicebear.com/7.x/bottts/svg?seed=CodeOrbit")
    is_admin = Column(Boolean, default=False)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    gems = Column(Integer, default=100)
    onboarding_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    preferences = relationship("UserPreferences", back_populates="user", uselist=False, lazy="joined", cascade="all, delete-orphan")
    streak = relationship("LearningStreak", back_populates="user", uselist=False, lazy="joined", cascade="all, delete-orphan")
    xp_transactions = relationship("XPTransaction", back_populates="user", cascade="all, delete-orphan")
    topic_progress = relationship("TopicProgress", back_populates="user", cascade="all, delete-orphan")
    question_attempts = relationship("UserQuestionAttempt", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    daily_quests = relationship("UserDailyQuest", back_populates="user", cascade="all, delete-orphan")
    challenge_attempts = relationship("ChallengeAttempt", back_populates="user", cascade="all, delete-orphan")
    study_plans = relationship("StudyPlan", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    ai_recommendations = relationship("AIRecommendation", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    interview_attempts = relationship("InterviewAttempt", back_populates="user", cascade="all, delete-orphan")

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    programming_level = Column(String(50), default="Intermediate")
    preferred_subjects = Column(Text, default="DBMS,DS,OS")
    daily_target_minutes = Column(Integer, default=30)
    career_goal = Column(String(100), default="Placement preparation")
    theme = Column(String(20), default="dark")
    sound_effects = Column(Boolean, default=True)
    daily_reminder = Column(Boolean, default=True)

    user = relationship("User", back_populates="preferences")

class LearningStreak(Base):
    __tablename__ = "learning_streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(Date, nullable=True)
    freeze_count = Column(Integer, default=1)
    # comma-separated days or JSON representation e.g. "M,T,W,T,F,S,S"
    weekly_history = Column(String(50), default="")

    user = relationship("User", back_populates="streak")

class XPTransaction(Base):
    __tablename__ = "xp_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="xp_transactions")
