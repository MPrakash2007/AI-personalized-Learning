from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date

class StudyPlanCreate(BaseModel):
    title: str
    subject_name: Optional[str] = None
    topic_name: Optional[str] = None
    scheduled_time: str = "5:00 PM"
    scheduled_date: date

class StudyPlanResponse(BaseModel):
    id: int
    title: str
    subject_name: Optional[str] = None
    topic_name: Optional[str] = None
    scheduled_time: str
    scheduled_date: date
    is_completed: bool

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    title: str
    content: str
    subject_id: Optional[int] = None
    topic_id: Optional[int] = None
    tags: Optional[str] = ""

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    subject_id: Optional[int] = None
    topic_id: Optional[int] = None
    tags: Optional[str] = None

class NoteResponse(BaseModel):
    id: int
    subject_id: Optional[int] = None
    topic_id: Optional[int] = None
    subject_name: Optional[str] = None
    topic_name: Optional[str] = None
    title: str
    content: str
    tags: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AIRecommendationResponse(BaseModel):
    id: int
    category: str
    title: str
    reason: str
    estimated_minutes: int
    action_url: str
    created_at: datetime

    class Config:
        from_attributes = True

class SubjectMasteryStat(BaseModel):
    subject_id: int
    name: str
    slug: str
    icon: str
    color: str
    mastery: float
    accuracy: float
    completed_topics: int
    total_topics: int

class WeakTopicStat(BaseModel):
    topic_id: int
    subject_name: str
    topic_title: str
    accuracy: float
    attempts_count: int
    recommendation: str

class ProgressOverviewResponse(BaseModel):
    total_xp: int
    current_level: int
    current_streak: int
    longest_streak: int
    overall_mastery: float
    overall_accuracy: float
    total_questions_attempted: int
    total_correct_answers: int
    topics_completed: int
    topics_mastered: int
    subject_mastery: List[SubjectMasteryStat]
    weak_topics: List[WeakTopicStat]
    xp_history: List[Dict[str, Any]]
    accuracy_history: List[Dict[str, Any]]
