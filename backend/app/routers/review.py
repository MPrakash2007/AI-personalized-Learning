from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.models.user import User
from app.models.learning import Question, Topic, Subject
from app.schemas.learning import QuestionResponse
from app.auth.deps import get_current_user
from app.services.review_service import get_due_for_review_topics

router = APIRouter(prefix="/review", tags=["Smart Review"])

@router.get("/due")
def get_due_reviews(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    due = get_due_for_review_topics(db, current_user.id)
    return {"due_topics": due}

@router.get("/session/{topic_id}", response_model=List[QuestionResponse])
def get_review_session_questions(topic_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    questions = db.query(Question).filter(Question.topic_id == topic.id).limit(5).all()
    return questions
