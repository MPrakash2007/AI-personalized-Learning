from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class QuickCheckQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str

class ChatMessageRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    session_id: Optional[int] = None
    subject: Optional[str] = None
    subject_id: Optional[int] = None
    topic: Optional[str] = None
    topic_id: Optional[int] = None
    action: Optional[str] = None  # explain_simply, exam_answer, give_example, mcqs, summarize, explain_code, interview_questions
    marks: Optional[int] = None   # 2, 5, 10

class ChatMessageResponse(BaseModel):
    id: int
    sender: str
    role: Optional[str] = None
    message: str
    content: Optional[str] = None
    conversation_id: Optional[int] = None
    session_id: Optional[int] = None
    quick_check: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChatResponse(BaseModel):
    answer: str
    conversation_id: int
    session_id: int
    message: str
    suggested_followups: List[str] = []
    sources: List[Dict[str, Any]] = []
    model: str = "gpt-4o-mini"
    quick_check: Optional[Dict[str, Any]] = None

class CreateConversationRequest(BaseModel):
    subject: Optional[str] = None
    subject_id: Optional[int] = None
    title: Optional[str] = None

class ChatSessionResponse(BaseModel):
    id: int
    conversation_id: Optional[int] = None
    title: str
    subject: Optional[str] = None
    subject_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0
    messages: List[ChatMessageResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ExplainMistakeRequest(BaseModel):
    question_id: int
    user_answer: str

class ExplainMistakeResponse(BaseModel):
    why_wrong: str
    core_concept: str
    real_world_example: str
    similar_question: Dict[str, Any]
