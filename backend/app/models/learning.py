from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    icon = Column(String(20), default="📚")
    description = Column(Text, nullable=False)
    color = Column(String(50), default="#8b5cf6")
    order = Column(Integer, default=0)

    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan", order_by="Topic.order")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), index=True, nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    is_boss = Column(Boolean, default=False)
    boss_title = Column(String(200), nullable=True)

    subject = relationship("Subject", back_populates="topics")
    lessons = relationship("Lesson", back_populates="topic", cascade="all, delete-orphan", order_by="Lesson.order")
    questions = relationship("Question", back_populates="topic", cascade="all, delete-orphan")
    topic_progress = relationship("TopicProgress", back_populates="topic", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    xp_reward = Column(Integer, default=50)
    estimated_minutes = Column(Integer, default=8)
    order = Column(Integer, default=0)

    topic = relationship("Topic", back_populates="lessons")
    steps = relationship("LessonStep", back_populates="lesson", cascade="all, delete-orphan", order_by="LessonStep.step_number")
    questions = relationship("Question", back_populates="lesson")

class LessonStep(Base):
    __tablename__ = "lesson_steps"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, default=1)
    step_type = Column(String(50), default="understand")  # understand, example, practice, apply, challenge, quiz
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    code_snippet = Column(Text, nullable=True)
    interactive_data = Column(Text, nullable=True)  # JSON for interactive step checkpoints

    lesson = relationship("Lesson", back_populates="steps")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True)
    prompt = Column(Text, nullable=False)
    question_type = Column(String(50), default="mcq")  # mcq, multi_select, fill_blank, true_false, match_concepts, arrange_order, predict_output, find_bug, code_completion, sql_challenge, diagram_interpretation, scenario, short_answer, difficulty_challenge
    difficulty = Column(String(20), default="MEDIUM")  # EASY, MEDIUM, HARD
    xp_reward = Column(Integer, default=10)
    explanation = Column(Text, nullable=False)
    code_snippet = Column(Text, nullable=True)
    is_important = Column(Boolean, default=False)
    metadata_json = Column(Text, nullable=True)  # extra structured params (pairs, sequence, sql schema)

    topic = relationship("Topic", back_populates="questions")
    lesson = relationship("Lesson", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan", order_by="QuestionOption.order")
    attempts = relationship("UserQuestionAttempt", back_populates="question", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="question", cascade="all, delete-orphan")

class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    explanation = Column(Text, nullable=True)
    order = Column(Integer, default=0)

    question = relationship("Question", back_populates="options")

class UserQuestionAttempt(Base):
    __tablename__ = "user_question_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    selected_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_taken_seconds = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="question_attempts")
    question = relationship("Question", back_populates="attempts")

class TopicProgress(Base):
    __tablename__ = "topic_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="LOCKED")  # LOCKED, AVAILABLE, IN_PROGRESS, COMPLETED, MASTERED, AI_RECOMMENDED
    mastery_score = Column(Float, default=0.0)
    accuracy = Column(Float, default=0.0)
    recent_accuracy = Column(Float, default=0.0)
    attempts_count = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    completed_steps = Column(Integer, default=0)
    total_steps = Column(Integer, default=6)
    last_practiced_at = Column(DateTime, nullable=True)
    next_review_due = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="topic_progress")
    topic = relationship("Topic", back_populates="topic_progress")

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="bookmarks")
    question = relationship("Question", back_populates="bookmarks")
