from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List

from app.config import settings
from app.database import engine, Base, get_db, SessionLocal
import app.models  # Ensures all SQLAlchemy models are registered

# Import routers
from app.routers.auth import router as auth_router
from app.routers.subjects import router as subjects_router
from app.routers.topics import router as topics_router
from app.routers.lessons import router as lessons_router
from app.routers.questions import router as questions_router
from app.routers.attempts import router as attempts_router
from app.routers.progress import router as progress_router
from app.routers.recommendations import router as recommendations_router
from app.routers.review import router as review_router
from app.routers.ai import router as ai_router
from app.routers.quests import router as quests_router
from app.routers.challenges import router as challenges_router
from app.routers.achievements import router as achievements_router
from app.routers.leaderboard import router as leaderboard_router
from app.routers.planner import router as planner_router
from app.routers.notes import router as notes_router
from app.routers.career import router as career_router
from app.routers.admin import router as admin_router
from app.routers.practice import router as practice_router

from app.models.learning import Subject, Topic, Question
from app.models.career import CareerQuestion

# Automatically initialize database schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CodeOrbit API",
    description="Backend REST API for CodeOrbit - AI Personalized Learning Platform for Engineering Students",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all API routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(subjects_router, prefix=settings.API_V1_STR)
app.include_router(topics_router, prefix=settings.API_V1_STR)
app.include_router(lessons_router, prefix=settings.API_V1_STR)
app.include_router(questions_router, prefix=settings.API_V1_STR)
app.include_router(practice_router, prefix=settings.API_V1_STR)
app.include_router(attempts_router, prefix=settings.API_V1_STR)
app.include_router(progress_router, prefix=settings.API_V1_STR)
app.include_router(recommendations_router, prefix=settings.API_V1_STR)
app.include_router(review_router, prefix=settings.API_V1_STR)
app.include_router(ai_router, prefix=settings.API_V1_STR)
app.include_router(quests_router, prefix=settings.API_V1_STR)
app.include_router(challenges_router, prefix=settings.API_V1_STR)
app.include_router(achievements_router, prefix=settings.API_V1_STR)
app.include_router(leaderboard_router, prefix=settings.API_V1_STR)
app.include_router(planner_router, prefix=settings.API_V1_STR)
app.include_router(notes_router, prefix=settings.API_V1_STR)
app.include_router(career_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def on_startup():
    """Auto-seeds fresh database (e.g. newly provisioned Postgres on Vercel) if empty."""
    try:
        db = SessionLocal()
        if db.query(Subject).count() == 0:
            from seed import seed_database
            seed_database(reset=False)
        db.close()
    except Exception as e:
        print(f"Startup check notice: {e}")

@app.get("/")
@app.get("/api")
@app.get("/api/")
def root():
    return {
        "app": "CodeOrbit",
        "description": "AI Personalized Learning Platform for Engineering Students",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }

@app.get(f"{settings.API_V1_STR}/search")
def global_search(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    """Global search across Subjects, Topics, and Career resources."""
    query_fmt = f"%{q.lower()}%"
    
    subjects = db.query(Subject).filter(
        (Subject.name.ilike(query_fmt)) | (Subject.description.ilike(query_fmt))
    ).limit(5).all()

    topics = db.query(Topic).filter(
        (Topic.title.ilike(query_fmt)) | (Topic.description.ilike(query_fmt))
    ).limit(8).all()

    career_items = db.query(CareerQuestion).filter(
        (CareerQuestion.title.ilike(query_fmt)) | (CareerQuestion.problem_statement.ilike(query_fmt))
    ).limit(6).all()

    return {
        "query": q,
        "subjects": [
            {"id": s.id, "name": s.name, "slug": s.slug, "icon": s.icon, "url": f"/learn/{s.slug}"}
            for s in subjects
        ],
        "topics": [
            {
                "id": t.id,
                "title": t.title,
                "subject_name": t.subject.name if t.subject else "General",
                "url": f"/learn/{t.subject.slug if t.subject else 'dbms'}/{t.slug}"
            }
            for t in topics
        ],
        "career": [
            {"id": c.id, "title": c.title, "category": c.category, "url": f"/career"}
            for c in career_items
        ]
    }
