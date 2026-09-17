from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from app.database import get_db
from app.models.user import User
from app.models.gamification import Challenge, ChallengeAttempt
from app.models.learning import Question, Subject
from app.schemas.gamification import ChallengeResponse, ChallengeSubmitRequest, ChallengeSubmitResponse
from app.schemas.learning import QuestionResponse
from app.auth.deps import get_current_user
from app.services.gamification_service import award_xp, update_user_streak, unlock_achievement

router = APIRouter(prefix="/challenges", tags=["Challenges"])

@router.get("", response_model=List[ChallengeResponse])
def get_challenges(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    challenges = db.query(Challenge).all()
    results = []

    for c in challenges:
        attempt = db.query(ChallengeAttempt).filter(
            ChallengeAttempt.user_id == current_user.id,
            ChallengeAttempt.challenge_id == c.id
        ).order_by(ChallengeAttempt.score.desc()).first()

        results.append(ChallengeResponse(
            id=c.id,
            title=c.title,
            challenge_type=c.challenge_type,
            subject_id=c.subject_id,
            description=c.description,
            duration_minutes=c.duration_minutes,
            xp_reward=c.xp_reward,
            questions_count=c.questions_count,
            is_completed=attempt is not None,
            best_score=attempt.score if attempt else None
        ))

    return results

@router.get("/{id}")
def get_challenge_detail(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    challenge = db.query(Challenge).filter(Challenge.id == id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    # Fetch questions for this challenge
    query = db.query(Question)
    if challenge.subject_id:
        query = query.filter(Question.topic.has(subject_id=challenge.subject_id))
    
    questions = query.limit(challenge.questions_count).all()

    return {
        "challenge": ChallengeResponse(
            id=challenge.id,
            title=challenge.title,
            challenge_type=challenge.challenge_type,
            subject_id=challenge.subject_id,
            description=challenge.description,
            duration_minutes=challenge.duration_minutes,
            xp_reward=challenge.xp_reward,
            questions_count=challenge.questions_count,
            is_completed=False,
            best_score=None
        ),
        "questions": [QuestionResponse.model_validate(q) for q in questions]
    }

@router.post("/submit", response_model=ChallengeSubmitResponse)
def submit_challenge_attempt(
    req: ChallengeSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    challenge = db.query(Challenge).filter(Challenge.id == req.challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    attempt = ChallengeAttempt(
        user_id=current_user.id,
        challenge_id=challenge.id,
        score=req.score,
        accuracy=req.accuracy,
        time_spent_seconds=req.time_spent_seconds
    )
    db.add(attempt)
    db.commit()

    # Award XP
    xp_to_award = challenge.xp_reward if req.accuracy >= 60.0 else int(challenge.xp_reward * 0.5)
    new_xp, new_level, _ = award_xp(db, current_user, xp_to_award, f"Completed Challenge: {challenge.title}")
    update_user_streak(db, current_user.id)

    if challenge.challenge_type == "boss" and req.accuracy >= 70.0:
        unlock_achievement(db, current_user.id, "first_boss")

    return ChallengeSubmitResponse(
        xp_earned=xp_to_award,
        new_xp=new_xp,
        new_level=new_level,
        message=f"Challenge submitted successfully! You earned +{xp_to_award} XP."
    )
