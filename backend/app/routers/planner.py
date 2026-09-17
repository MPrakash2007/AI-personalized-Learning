from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone, date
from app.database import get_db
from app.models.user import User
from app.models.analytics import StudyPlan
from app.schemas.analytics import StudyPlanCreate, StudyPlanResponse
from app.auth.deps import get_current_user

router = APIRouter(prefix="/planner", tags=["Study Planner"])

@router.get("", response_model=List[StudyPlanResponse])
def get_study_plans(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plans = db.query(StudyPlan).filter(
        StudyPlan.user_id == current_user.id
    ).order_by(StudyPlan.scheduled_date.asc(), StudyPlan.scheduled_time.asc()).all()
    return plans

@router.post("", response_model=StudyPlanResponse)
def create_study_plan(
    plan_in: StudyPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = StudyPlan(
        user_id=current_user.id,
        title=plan_in.title,
        subject_name=plan_in.subject_name,
        topic_name=plan_in.topic_name,
        scheduled_time=plan_in.scheduled_time,
        scheduled_date=plan_in.scheduled_date,
        is_completed=False
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

@router.put("/{id}/toggle", response_model=StudyPlanResponse)
def toggle_study_plan(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = db.query(StudyPlan).filter(
        StudyPlan.id == id,
        StudyPlan.user_id == current_user.id
    ).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Task not found")

    plan.is_completed = not plan.is_completed
    db.commit()
    db.refresh(plan)
    return plan

@router.delete("/{id}")
def delete_study_plan(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = db.query(StudyPlan).filter(
        StudyPlan.id == id,
        StudyPlan.user_id == current_user.id
    ).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(plan)
    db.commit()
    return {"message": "Task deleted successfully"}
