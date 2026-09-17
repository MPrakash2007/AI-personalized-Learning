from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.learning import Topic, Lesson, LessonStep, Question, TopicProgress
from app.models.user import User
from app.schemas.learning import TopicResponse, TopicProgressResponse, LessonResponse, QuestionResponse, QuestionOptionResponse
from app.auth.deps import get_current_user

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("/{slug_or_id}")
def get_topic_detail(slug_or_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if slug_or_id.isdigit():
        topic = db.query(Topic).filter(Topic.id == int(slug_or_id)).first()
    else:
        topic = db.query(Topic).filter(Topic.slug == slug_or_id.lower()).first()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Fetch user topic progress
    progress = db.query(TopicProgress).filter(
        TopicProgress.user_id == current_user.id,
        TopicProgress.topic_id == topic.id
    ).first()

    prog_data = TopicProgressResponse.model_validate(progress) if progress else TopicProgressResponse(
        topic_id=topic.id,
        status="AVAILABLE",
        mastery_score=0.0,
        accuracy=0.0,
        recent_accuracy=0.0,
        attempts_count=0,
        correct_count=0,
        completed_steps=0,
        total_steps=6
    )

    # Fetch lessons and steps
    lessons = db.query(Lesson).filter(Lesson.topic_id == topic.id).order_by(Lesson.order.asc()).all()
    questions = db.query(Question).filter(Question.topic_id == topic.id).all()

    formatted_lessons = []
    for l in lessons:
        formatted_lessons.append(LessonResponse.model_validate(l))

    formatted_questions = []
    for q in questions:
        formatted_questions.append(QuestionResponse.model_validate(q))

    return {
        "id": topic.id,
        "subject_id": topic.subject_id,
        "subject_slug": topic.subject.slug if topic.subject else "dbms",
        "subject_name": topic.subject.name if topic.subject else "DBMS",
        "subject_icon": topic.subject.icon if topic.subject else "🗄️",
        "title": topic.title,
        "slug": topic.slug,
        "description": topic.description,
        "order": topic.order,
        "is_boss": topic.is_boss,
        "boss_title": topic.boss_title,
        "progress": prog_data,
        "lessons": formatted_lessons,
        "questions": formatted_questions
    }
