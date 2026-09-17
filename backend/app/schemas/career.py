from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class CareerQuestionResponse(BaseModel):
    id: int
    category: str
    sub_topic: str
    company_tag: str
    difficulty: str
    title: str
    problem_statement: str
    options_json: Optional[str] = None
    solution_hint: Optional[str] = None
    xp_reward: int

    class Config:
        from_attributes = True

class CareerQuestionSubmit(BaseModel):
    question_id: int
    selected_answer: str

class InterviewSubmitRequest(BaseModel):
    career_question_id: Optional[int] = None
    question_prompt: str
    student_answer: str

class InterviewFeedbackResponse(BaseModel):
    overall_score: int
    feedback_clarity: str
    feedback_depth: str
    feedback_structure: str
    feedback_missing: str
    feedback_suggestions: str
    xp_earned: int = 25

class CompanyGuide(BaseModel):
    category_id: str
    name: str
    description: str
    target_roles: List[str]
    key_subjects: List[str]
    common_dsa_topics: List[str]
    rounds_breakdown: List[str]
    checklist: List[str]
