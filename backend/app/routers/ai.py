import json
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

router = APIRouter(prefix="/ai", tags=["AI Tutor"])

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

    if not session:
        subject_name = "General CS"
        if req.subject_id:
            subj = db.query(Subject).filter(Subject.id == req.subject_id).first()
            if subj:
                subject_name = subj.name
        session = ChatSession(
            user_id=current_user.id,
            subject_id=req.subject_id,
            title=f"{subject_name} Tutoring"
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # Save student message
    student_msg = ChatMessage(
        session_id=session.id,
        sender="student",
        message=req.message
    )
    db.add(student_msg)
    db.commit()

    # Query AI provider
    provider = get_ai_provider()
    context = session.title if session else "Computer Science"
    ai_reply_text, quick_check_data = provider.chat_tutor(req.message, context=context)

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
        "quick_check": quick_check_data
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
