from pydantic import BaseModel
from typing import Optional, List, Any, Dict
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
    question_context: Optional[str] = "LEARN"
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    source_type: Optional[str] = None
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
    section_order: Optional[int] = 1
    section_type: Optional[str] = "concept"
    example_data: Optional[str] = None
    diagram_data: Optional[str] = None
    source_name: Optional[str] = None
    source_url: Optional[str] = None

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
    is_accessible: bool = True
    is_completed: bool = False
    is_current: bool = False
    is_next: bool = False

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
    is_accessible: bool = True
    is_completed: bool = False
    status: str = "AVAILABLE"
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

class QuizCompleteRequest(BaseModel):
    score: Optional[int] = None
    total: Optional[int] = None
    answers: Optional[List[Dict[str, Any]]] = None
    time_taken_seconds: int = 0

class QuizCompleteResponse(BaseModel):
    topic_id: int
    topic_slug: str
    status: str
    mastery_score: float
    mastery_level: str
    xp_earned: int
    xp_awarded: int
    new_xp: int
    new_level: int
    level_up: bool
    next_topic_slug: Optional[str] = None
    next_topic_title: Optional[str] = None
    unlocked_next: bool = False

class QuickReferenceResponse(BaseModel):
    topic_slug: str
    title: str
    subject: str
    exam_definition: str
    remember: str
    core_concept: str
    key_points: List[str]
    classification: Any
    how_it_works: Any
    example: Any
    comparison: Any
    formulas: List[Any]
    exam_tip: str
    common_confusion: Any
    faqs: List[Any]
    revision_60s: List[str]
    references: List[Any]
