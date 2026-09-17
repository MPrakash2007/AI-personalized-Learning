from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.models.user import User
from app.auth.deps import get_current_user
from app.services.recommendation_service import generate_user_recommendations, sync_recommendations_to_database

router = APIRouter(prefix="/recommendations", tags=["AI Recommendations"])

@router.get("")
def get_recommendations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recs = generate_user_recommendations(db, current_user.id)
    return {"recommendations": recs}

@router.post("/generate")
def refresh_recommendations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sync_recommendations_to_database(db, current_user.id)
    recs = generate_user_recommendations(db, current_user.id)
    return {"message": "Recommendations refreshed", "recommendations": recs}
