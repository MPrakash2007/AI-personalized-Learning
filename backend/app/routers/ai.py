from datetime import datetime, timezone
import json
import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.user import User
from app.models.ai import ChatSession, ChatMessage
from app.models.learning import Question, Subject, Topic, TopicProgress
from app.schemas.ai import (
    ChatMessageRequest,
    ChatResponse,
    ChatSessionResponse,
    ChatMessageResponse,
    CreateConversationRequest,
    ExplainMistakeRequest,
    ExplainMistakeResponse,
)
from app.auth.deps import get_current_user
from app.services.ai_tutor import get_ai_tutor_service
from app.services.ai_service import get_ai_provider
from app.config import settings
from app.services.gamification_service import unlock_achievement
from app.services.retrieval_service import search_educational_knowledge

logger = logging.getLogger(__name__)

router = APIRouter(tags=["AI Tutor"])

@router.get("/status")
def get_ai_tutor_status():
    """Safe diagnostic endpoint reporting AI Tutor configuration status without secrets."""
    import os
    service = get_ai_tutor_service()
    ai_keys = [
        k for k in os.environ.keys()
        if any(term in k.upper() for term in ("OPENAI", "AI_", "GPT", "_AI"))
    ]
    return {
        "configured": service.is_configured(),
        "provider": settings.get_ai_provider(),
        "model": service.model,
        "detected_env_keys": sorted(ai_keys),
    }

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
    """
    Open-ended AI Tutor Chat endpoint.
    Dynamically answers any student academic or technical question using OpenAI.
    Maintains multi-turn context and supports curriculum context without restriction.
    """
    clean_msg = req.message.strip()
    if not clean_msg:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty.")
    if len(clean_msg) > 4000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message exceeds maximum allowed length of 4000 characters.")

    target_id = req.conversation_id or req.session_id
    session = None

    if target_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == target_id,
            ChatSession.user_id == current_user.id
        ).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied."
            )

    subject_name = req.subject
    if req.subject_id and not subject_name:
        subj = db.query(Subject).filter(Subject.id == req.subject_id).first()
        if subj:
            subject_name = subj.name

    if not session:
        # Generate initial conversation title from the first question
        title = clean_msg[:42].strip()
        if len(clean_msg) > 42:
            title += "..."
        session = ChatSession(
            user_id=current_user.id,
            subject_id=req.subject_id,
            subject=subject_name,
            title=title or "Study Session"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
    else:
        # Update subject context if provided on follow-up
        if subject_name and not session.subject:
            session.subject = subject_name
            db.commit()

    # Save student message
    student_msg = ChatMessage(
        session_id=session.id,
        sender="user",
        message=clean_msg
    )
    db.add(student_msg)
    db.commit()

    # Fetch recent conversation history (last 10 turns) for multi-turn coreference resolution
    past_messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id,
        ChatMessage.id != student_msg.id
    ).order_by(ChatMessage.created_at.asc()).all()[-10:]

    history_payload = [
        {
            "role": "user" if m.sender in ("student", "user") else "assistant",
            "content": m.message
        }
        for m in past_messages
    ]

    # Gather optional student learning context (completed topics, level)
    student_ctx: Dict[str, Any] = {
        "level": current_user.level,
        "xp": current_user.xp,
    }
    try:
        completed_topics = (
            db.query(Topic.title)
            .join(TopicProgress, TopicProgress.topic_id == Topic.id)
            .filter(TopicProgress.user_id == current_user.id, TopicProgress.status.in_(["COMPLETED", "MASTERED"]))
            .limit(6)
            .all()
        )
        if completed_topics:
            student_ctx["completed_topics"] = [t[0] for t in completed_topics]
    except Exception:
        pass

    # Optional retrieval grounding check for references and quick checks
    retrieval_data = search_educational_knowledge(db, clean_msg, subject_slug=session.subject)
    quick_check_data = retrieval_data.get("quick_check") if retrieval_data else None
    sources_data = retrieval_data.get("sources", []) if retrieval_data else []

    if not quick_check_data:
        quick_check_data = {
            "question": f"In computer science systems, what core design principle ensures correctness when evaluating {clean_msg[:40]}?",
            "options": [
                "Invariant validation & modular abstraction",
                "Unbounded global state mutation",
                "Tight component coupling",
                "Suppressing boundary exception checks"
            ],
            "correct_answer": "Invariant validation & modular abstraction",
            "explanation": "Systems engineering mandates strict modular abstraction and invariant preservation across state transitions."
        }

    if not sources_data:
        sources_data = [
            {"source_name": "GeeksforGeeks", "name": "GeeksforGeeks", "source_url": "https://www.geeksforgeeks.org/computer-science-projects/", "url": "https://www.geeksforgeeks.org/computer-science-projects/", "title": "Computer Science Knowledge Base"},
            {"source_name": "TutorialsPoint", "name": "TutorialsPoint", "source_url": "https://www.tutorialspoint.com/computer_science_tutorials.htm", "url": "https://www.tutorialspoint.com/computer_science_tutorials.htm", "title": "TutorialsPoint Engineering Reference"}
        ]

    # Query OpenAI Tutor Service
    tutor_service = get_ai_tutor_service()
    answer_text, suggested_followups, model_used = tutor_service.generate_response(
        message=clean_msg,
        conversation_history=history_payload,
        subject=session.subject or subject_name,
        action=req.action,
        marks=req.marks,
        student_context=student_ctx,
    )

    # Save AI response
    ai_msg = ChatMessage(
        session_id=session.id,
        sender="assistant",
        message=answer_text,
        quick_check_json=json.dumps(quick_check_data) if quick_check_data else None
    )
    session.updated_at = datetime.now(timezone.utc)
    db.add(ai_msg)
    db.commit()

    # Track achievement for active AI tutoring engagement
    total_ai_msgs = db.query(ChatMessage).join(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatMessage.sender.in_(["student", "user"])
    ).count()
    if total_ai_msgs >= 10:
        unlock_achievement(db, current_user.id, "ai_tutor_10")

    return {
        "answer": answer_text,
        "conversation_id": session.id,
        "session_id": session.id,
        "message": answer_text,
        "reply": answer_text,
        "quick_check": quick_check_data,
        "sources": sources_data,
        "suggested_followups": suggested_followups,
        "model": model_used
    }


@router.get("/conversations")
@router.get("/sessions")
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all AI Tutor conversations belonging to the current user."""
    sessions = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == current_user.id)
        .order_by(ChatSession.updated_at.desc())
        .all()
    )

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
                "conversation_id": s.id,
                "session_id": s.id,
                "sender": m.sender,
                "role": "user" if m.sender in ("student", "user") else "assistant",
                "message": m.message,
                "content": m.message,
                "quick_check": qc,
                "created_at": m.created_at
            })
        results.append({
            "id": s.id,
            "conversation_id": s.id,
            "title": s.title,
            "subject": s.subject,
            "subject_id": s.subject_id,
            "created_at": s.created_at,
            "updated_at": s.updated_at,
            "message_count": len(msgs),
            "messages": msgs
        })

    return results


@router.get("/conversations/{conversation_id}")
def get_single_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a single conversation and its messages. Verifies user ownership."""
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == conversation_id, ChatSession.user_id == current_user.id)
        .first()
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied."
        )

    msgs = []
    for m in session.messages:
        qc = None
        if m.quick_check_json:
            try:
                qc = json.loads(m.quick_check_json)
            except Exception:
                pass
        msgs.append({
            "id": m.id,
            "conversation_id": session.id,
            "session_id": session.id,
            "sender": m.sender,
            "role": "user" if m.sender in ("student", "user") else "assistant",
            "message": m.message,
            "content": m.message,
            "quick_check": qc,
            "created_at": m.created_at
        })

    return {
        "id": session.id,
        "conversation_id": session.id,
        "title": session.title,
        "subject": session.subject,
        "subject_id": session.subject_id,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "message_count": len(msgs),
        "messages": msgs
    }


@router.post("/conversations")
def create_new_conversation(
    req: CreateConversationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creates a new AI Tutor conversation."""
    title = req.title or (f"{req.subject} Study Session" if req.subject else "New Study Chat")
    session = ChatSession(
        user_id=current_user.id,
        subject=req.subject,
        subject_id=req.subject_id,
        title=title
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return {
        "id": session.id,
        "conversation_id": session.id,
        "title": session.title,
        "subject": session.subject,
        "subject_id": session.subject_id,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "messages": []
    }


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletes an entire conversation. Enforces user ownership."""
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == conversation_id, ChatSession.user_id == current_user.id)
        .first()
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied."
        )

    db.delete(session)
    db.commit()
    return {"status": "deleted", "conversation_id": conversation_id}


@router.post("/conversations/{conversation_id}/clear")
def clear_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Clears all messages inside a conversation. Enforces user ownership."""
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == conversation_id, ChatSession.user_id == current_user.id)
        .first()
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied."
        )

    db.query(ChatMessage).filter(ChatMessage.session_id == session.id).delete()
    session.updated_at = datetime.now(timezone.utc)
    db.commit()
    return {"status": "cleared", "conversation_id": conversation_id}


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
