from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class QuickCheckQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str

class ChatMessageRequest(BaseModel):
    message: str
    subject_id: Optional[int] = None
    session_id: Optional[int] = None

class ChatMessageResponse(BaseModel):
    id: int
    sender: str
    message: str
    quick_check: Optional[QuickCheckQuestion] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSessionResponse(BaseModel):
    id: int
    title: str
    subject_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True

class ExplainMistakeRequest(BaseModel):
    question_id: int
    user_answer: str

class ExplainMistakeResponse(BaseModel):
    why_wrong: str
    core_concept: str
    real_world_example: str
    similar_question: Dict[str, Any]
