import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.ai import ChatSession, ChatMessage
from app.models.learning import Question, Subject
from app.schemas.ai import ChatMessageRequest, ExplainMistakeRequest, ExplainMistakeResponse
from app.auth.deps import get_current_user
from app.services.ai_service import get_ai_provider
from app.services.gamification_service import unlock_achievement
from app.services.retrieval_service import search_educational_knowledge

router = APIRouter(prefix="/ai", tags=["AI Tutor"])

@router.get("/search")
def search_ai_knowledge(
    q: Optional[str] = None,
    query: Optional[str] = None,
    subject: Optional[str] = None,
    subject_slug: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve grounded curriculum context, relevant questions, and source references."""
    search_query = q or query or ""
    subj_filter = subject or subject_slug
    return search_educational_knowledge(db, search_query, subject_slug=subj_filter)

@router.post("/chat")
def chat_with_tutor(
    req: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find or create chat session
    session = None
    if req.session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == req.session_id,
            ChatSession.user_id == current_user.id
        ).first()

    subject_slug = None
    if not session:
        subject_name = "General CS"
        if req.subject_id:
            subj = db.query(Subject).filter(Subject.id == req.subject_id).first()
            if subj:
                subject_name = subj.name
                subject_slug = subj.slug
        session = ChatSession(
            user_id=current_user.id,
            subject_id=req.subject_id,
            title=f"{subject_name} Tutoring"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
    elif session.subject_id:
        subj = db.query(Subject).filter(Subject.id == session.subject_id).first()
        if subj:
            subject_slug = subj.slug

    # Save student message
    student_msg = ChatMessage(
        session_id=session.id,
        sender="student",
        message=req.message
    )
    db.add(student_msg)
    db.commit()

    # Search local database curriculum content
    retrieval_data = search_educational_knowledge(db, req.message, subject_slug=subject_slug)

    # Query AI provider with grounded retrieval context
    provider = get_ai_provider()
    context = session.title if session else "Computer Science"
    ai_reply_text, quick_check_data, sources = provider.chat_tutor(
        req.message, context=context, retrieval_data=retrieval_data
    )

    # Save AI response
    ai_msg = ChatMessage(
        session_id=session.id,
        sender="ai",
        message=ai_reply_text,
        quick_check_json=json.dumps(quick_check_data) if quick_check_data else None
    )
    db.add(ai_msg)
    db.commit()

    # Track achievement for using AI tutor
    total_ai_msgs = db.query(ChatMessage).join(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatMessage.sender == "student"
    ).count()
    if total_ai_msgs >= 10:
        unlock_achievement(db, current_user.id, "ai_tutor_10")

    return {
        "session_id": session.id,
        "message": ai_reply_text,
        "quick_check": quick_check_data,
        "sources": sources
    }


@router.get("/sessions")
def get_chat_sessions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(ChatSession.updated_at.desc()).all()

    results = []
    for s in sessions:
        msgs = []
        for m in s.messages:
            qc = None
            if m.quick_check_json:
                try:
                    qc = json.loads(m.quick_check_json)
                except Exception:
                    pass
            msgs.append({
                "id": m.id,
                "sender": m.sender,
                "message": m.message,
                "quick_check": qc,
                "created_at": m.created_at
            })
        results.append({
            "id": s.id,
            "title": s.title,
            "subject_id": s.subject_id,
            "created_at": s.created_at,
            "messages": msgs
        })

    return results

@router.post("/explain-mistake", response_model=ExplainMistakeResponse)
def explain_mistake(
    req: ExplainMistakeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = db.query(Question).filter(Question.id == req.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    correct_option = next((opt for opt in question.options if opt.is_correct), None)
    correct_text = correct_option.text if correct_option else "Correct Option"

    provider = get_ai_provider()
    explanation_data = provider.explain_mistake(
        question_prompt=question.prompt,
        user_answer=req.user_answer,
        correct_answer=correct_text,
        explanation=question.explanation
    )

    return explanation_data
