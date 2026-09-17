from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.learning import Question, QuestionOption, UserQuestionAttempt, TopicProgress, Topic
from app.models.user import User
from app.schemas.learning import AttemptSubmitRequest, AttemptSubmitResponse
from app.auth.deps import get_current_user
from app.services.progress_service import update_topic_progress_after_attempt
from app.services.gamification_service import award_xp, update_user_streak, update_daily_quest_progress, unlock_achievement
from app.services.recommendation_service import sync_recommendations_to_database

router = APIRouter(prefix="/attempts", tags=["Attempts"])

@router.post("/submit", response_model=AttemptSubmitResponse)
def submit_attempt(
    attempt_in: AttemptSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = db.query(Question).filter(Question.id == attempt_in.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Determine correctness
    # If options exist, check option with is_correct = True
    correct_option = next((opt for opt in question.options if opt.is_correct), None)
    
    is_correct = False
    correct_answer_str = ""

    if correct_option:
        correct_answer_str = correct_option.text
        # Compare text or option ID
        is_correct = (
            attempt_in.selected_answer.strip().lower() == correct_option.text.strip().lower() or
            attempt_in.selected_answer.strip() == str(correct_option.id)
        )
    else:
        # Fallback for text/blank answers stored in explanation or metadata
        correct_answer_str = "See detailed concept explanation"
        is_correct = True

    # Record attempt
    attempt = UserQuestionAttempt(
        user_id=current_user.id,
        question_id=question.id,
        topic_id=attempt_in.topic_id,
        selected_answer=attempt_in.selected_answer,
        is_correct=is_correct,
        time_taken_seconds=attempt_in.time_taken_seconds
    )
    db.add(attempt)
    db.commit()

    # Gamification: award XP
    xp_earned = 0
    if is_correct:
        # Base +5 XP, +10 if hard
        xp_earned = 10 if question.difficulty == "HARD" else 5
        if question.xp_reward:
            xp_earned = max(xp_earned, question.xp_reward)

    new_xp, new_level, level_up = award_xp(
        db, current_user, xp_earned, f"Answered question in {question.topic.title if question.topic else 'Topic'}"
    )

    # Streak update
    current_streak = update_user_streak(db, current_user.id)

    # Daily quests increment
    update_daily_quest_progress(db, current_user.id, "questions", 1)

    # Progress & Mastery update
    old_prog = db.query(TopicProgress).filter(
        TopicProgress.user_id == current_user.id,
        TopicProgress.topic_id == attempt_in.topic_id
    ).first()
    old_mastery = old_prog.mastery_score if old_prog else 0.0

    updated_prog = update_topic_progress_after_attempt(
        db, current_user.id, attempt_in.topic_id, is_correct
    )
    mastery_change = round(updated_prog.mastery_score - old_mastery, 1)

    # Check mastery achievement
    if updated_prog.mastery_score >= 85.0:
        unlock_achievement(db, current_user.id, "first_mastery")

    # Update recommendations asynchronously or on attempt
    recommendation_hint = None
    if not is_correct:
        recommendation_hint = f"Focus on {question.topic.title if question.topic else 'this concept'} to reinforce foundational understanding."
    elif updated_prog.mastery_score >= 85.0:
        recommendation_hint = f"Mastery achieved in {question.topic.title if question.topic else 'Topic'}! Ready to advance."

    return AttemptSubmitResponse(
        is_correct=is_correct,
        correct_answer=correct_answer_str,
        explanation=question.explanation,
        xp_earned=xp_earned,
        new_xp=new_xp,
        new_level=new_level,
        level_up=level_up,
        current_streak=current_streak,
        topic_mastery=updated_prog.mastery_score,
        mastery_change=mastery_change,
        status=updated_prog.status,
        recommendation_hint=recommendation_hint
    )
