from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from app.database import get_db
from app.models.user import User
from app.models.analytics import Note
from app.models.learning import Subject, Topic
from app.schemas.analytics import NoteCreate, NoteUpdate, NoteResponse
from app.auth.deps import get_current_user

router = APIRouter(prefix="/notes", tags=["My Notes"])

@router.get("", response_model=List[NoteResponse])
def get_notes(
    search: Optional[str] = None,
    subject_id: Optional[int] = None,
    topic_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Note).filter(Note.user_id == current_user.id)

    if subject_id:
        query = query.filter(Note.subject_id == subject_id)
    if topic_id:
        query = query.filter(Note.topic_id == topic_id)
    if search:
        search_fmt = f"%{search.lower()}%"
        query = query.filter(
            (Note.title.ilike(search_fmt)) |
            (Note.content.ilike(search_fmt)) |
            (Note.tags.ilike(search_fmt))
        )

    notes = query.order_by(Note.updated_at.desc()).all()
    results = []
    for n in notes:
        s_name = None
        t_name = None
        if n.subject_id:
            s = db.query(Subject).filter(Subject.id == n.subject_id).first()
            if s:
                s_name = s.name
        if n.topic_id:
            t = db.query(Topic).filter(Topic.id == n.topic_id).first()
            if t:
                t_name = t.title

        results.append(NoteResponse(
            id=n.id,
            subject_id=n.subject_id,
            topic_id=n.topic_id,
            subject_name=s_name,
            topic_name=t_name,
            title=n.title,
            content=n.content,
            tags=n.tags or "",
            created_at=n.created_at,
            updated_at=n.updated_at
        ))

    return results

@router.post("", response_model=NoteResponse)
def create_note(note_in: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = Note(
        user_id=current_user.id,
        subject_id=note_in.subject_id,
        topic_id=note_in.topic_id,
        title=note_in.title,
        content=note_in.content,
        tags=note_in.tags or ""
    )
    db.add(note)
    db.commit()
    db.refresh(note)

    s_name = None
    t_name = None
    if note.subject_id:
        s = db.query(Subject).filter(Subject.id == note.subject_id).first()
        if s:
            s_name = s.name
    if note.topic_id:
        t = db.query(Topic).filter(Topic.id == note.topic_id).first()
        if t:
            t_name = t.title

    return NoteResponse(
        id=note.id,
        subject_id=note.subject_id,
        topic_id=note.topic_id,
        subject_name=s_name,
        topic_name=t_name,
        title=note.title,
        content=note.content,
        tags=note.tags or "",
        created_at=note.created_at,
        updated_at=note.updated_at
    )

@router.put("/{id}", response_model=NoteResponse)
def update_note(id: int, note_in: NoteUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note_in.title is not None:
        note.title = note_in.title
    if note_in.content is not None:
        note.content = note_in.content
    if note_in.subject_id is not None:
        note.subject_id = note_in.subject_id
    if note_in.topic_id is not None:
        note.topic_id = note_in.topic_id
    if note_in.tags is not None:
        note.tags = note_in.tags

    note.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(note)

    s_name = None
    t_name = None
    if note.subject_id:
        s = db.query(Subject).filter(Subject.id == note.subject_id).first()
        if s:
            s_name = s.name
    if note.topic_id:
        t = db.query(Topic).filter(Topic.id == note.topic_id).first()
        if t:
            t_name = t.title

    return NoteResponse(
        id=note.id,
        subject_id=note.subject_id,
        topic_id=note.topic_id,
        subject_name=s_name,
        topic_name=t_name,
        title=note.title,
        content=note.content,
        tags=note.tags or "",
        created_at=note.created_at,
        updated_at=note.updated_at
    )

@router.delete("/{id}")
def delete_note(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}
