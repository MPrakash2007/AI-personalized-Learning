from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class CareerQuestion(Base):
    __tablename__ = "career_questions"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)  # dsa, mcq, interview_tech, interview_hr, interview_behavioral, interview_project, company_prep
    sub_topic = Column(String(100), nullable=False)  # Arrays, Trees, DBMS, System Design, HR, etc.
    company_tag = Column(String(100), default="Product Companies")
    difficulty = Column(String(20), default="MEDIUM")  # EASY, MEDIUM, HARD
    title = Column(String(255), nullable=False)
    problem_statement = Column(Text, nullable=False)
    options_json = Column(Text, nullable=True)  # JSON for MCQs
    correct_answer = Column(Text, nullable=True)
    solution_hint = Column(Text, nullable=True)
    xp_reward = Column(Integer, default=25)

    interview_attempts = relationship("InterviewAttempt", back_populates="career_question")

class InterviewAttempt(Base):
    __tablename__ = "interview_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_question_id = Column(Integer, ForeignKey("career_questions.id", ondelete="SET NULL"), nullable=True)
    question_prompt = Column(Text, nullable=False)
    student_answer = Column(Text, nullable=False)
    feedback_clarity = Column(Text, nullable=True)
    feedback_depth = Column(Text, nullable=True)
    feedback_structure = Column(Text, nullable=True)
    feedback_missing = Column(Text, nullable=True)
    feedback_suggestions = Column(Text, nullable=True)
    overall_score = Column(Integer, default=70)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="interview_attempts")
    career_question = relationship("CareerQuestion", back_populates="interview_attempts")
