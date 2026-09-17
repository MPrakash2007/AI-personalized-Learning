from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.learning import Question, QuestionOption, Bookmark, UserQuestionAttempt, Topic, Subject
from app.models.user import User
from app.schemas.learning import QuestionResponse, BookmarkCreate, BookmarkResponse
from app.auth.deps import get_current_user

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.get("", response_model=List[QuestionResponse])
def get_questions(
    subject_id: Optional[int] = None,
    topic_id: Optional[int] = None,
    difficulty: Optional[str] = None,
    question_type: Optional[str] = None,
    is_important: Optional[bool] = None,
    only_bookmarked: Optional[bool] = False,
    only_incorrect: Optional[bool] = False,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Question)

    if topic_id:
        query = query.filter(Question.topic_id == topic_id)
    elif subject_id:
        topic_ids = [t.id for t in db.query(Topic.id).filter(Topic.subject_id == subject_id).all()]
        query = query.filter(Question.topic_id.in_(topic_ids))

    if difficulty:
        query = query.filter(Question.difficulty == difficulty.upper())

    if question_type:
        query = query.filter(Question.question_type == question_type)

    if is_important is not None:
        query = query.filter(Question.is_important == is_important)

    if only_bookmarked:
        bookmarked_ids = [b.question_id for b in db.query(Bookmark.question_id).filter(Bookmark.user_id == current_user.id).all()]
        query = query.filter(Question.id.in_(bookmarked_ids))

    if only_incorrect:
        wrong_ids = [a.question_id for a in db.query(UserQuestionAttempt.question_id).filter(
            UserQuestionAttempt.user_id == current_user.id,
            UserQuestionAttempt.is_correct == False
        ).all()]
        query = query.filter(Question.id.in_(wrong_ids))

    return query.offset(offset).limit(limit).all()

@router.get("/bookmarks", response_model=List[BookmarkResponse])
def get_bookmarks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == current_user.id).order_by(Bookmark.created_at.desc()).all()
    return bookmarks

@router.post("/bookmark", response_model=BookmarkResponse)
def create_bookmark(b_in: BookmarkCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.question_id == b_in.question_id
    ).first()

    if existing:
        existing.note = b_in.note
        db.commit()
        db.refresh(existing)
        return existing

    new_bm = Bookmark(user_id=current_user.id, question_id=b_in.question_id, note=b_in.note)
    db.add(new_bm)
    db.commit()
    db.refresh(new_bm)
    return new_bm

@router.delete("/bookmark/{question_id}")
def delete_bookmark(question_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bm = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.question_id == question_id
    ).first()
    if not bm:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    db.delete(bm)
    db.commit()
    return {"message": "Bookmark removed"}

@router.get("/{id}", response_model=QuestionResponse)
def get_question(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    question = db.query(Question).filter(Question.id == id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question
