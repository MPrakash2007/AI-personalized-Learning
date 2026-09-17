from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class QuestionOptionResponse(BaseModel):
    id: int
    text: str
    order: int
    # Note: is_correct is excluded or optional depending on quiz mode to prevent client cheat
    is_correct: Optional[bool] = None
    explanation: Optional[str] = None

    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    id: int
    topic_id: int
    lesson_id: Optional[int] = None
    prompt: str
    question_type: str
    difficulty: str
    xp_reward: int
    code_snippet: Optional[str] = None
    explanation: Optional[str] = None
    is_important: bool = False
    metadata_json: Optional[str] = None
    options: List[QuestionOptionResponse] = []

    class Config:
        from_attributes = True

class LessonStepResponse(BaseModel):
    id: int
    step_number: int
    step_type: str
    title: str
    content: str
    code_snippet: Optional[str] = None
    interactive_data: Optional[str] = None

    class Config:
        from_attributes = True

class LessonResponse(BaseModel):
    id: int
    topic_id: int
    title: str
    xp_reward: int
    estimated_minutes: int
    order: int
    steps: List[LessonStepResponse] = []
    questions: List[QuestionResponse] = []

    class Config:
        from_attributes = True

class TopicProgressResponse(BaseModel):
    topic_id: int
    status: str
    mastery_score: float
    accuracy: float
    recent_accuracy: float
    attempts_count: int
    correct_count: int
    completed_steps: int
    total_steps: int
    last_practiced_at: Optional[datetime] = None
    next_review_due: Optional[datetime] = None

    class Config:
        from_attributes = True

class TopicResponse(BaseModel):
    id: int
    subject_id: int
    title: str
    slug: str
    description: Optional[str] = None
    order: int
    is_boss: bool
    boss_title: Optional[str] = None
    lessons_count: int = 0
    questions_count: int = 0
    progress: Optional[TopicProgressResponse] = None

    class Config:
        from_attributes = True

class SubjectResponse(BaseModel):
    id: int
    name: str
    slug: str
    icon: str
    description: str
    color: str
    order: int
    topics_count: int = 0
    completed_topics_count: int = 0
    progress_percentage: float = 0.0
    overall_mastery: float = 0.0

    class Config:
        from_attributes = True

class SubjectDetailResponse(SubjectResponse):
    topics: List[TopicResponse] = []

class AttemptSubmitRequest(BaseModel):
    question_id: int
    topic_id: int
    selected_answer: str
    time_taken_seconds: int = 0

class AttemptSubmitResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str
    xp_earned: int
    new_xp: int
    new_level: int
    level_up: bool
    current_streak: int
    topic_mastery: float
    mastery_change: float
    status: str
    recommendation_hint: Optional[str] = None

class BookmarkCreate(BaseModel):
    question_id: int
    note: Optional[str] = None

class BookmarkResponse(BaseModel):
    id: int
    question_id: int
    note: Optional[str] = None
    created_at: datetime
    question: Optional[QuestionResponse] = None

    class Config:
        from_attributes = True
