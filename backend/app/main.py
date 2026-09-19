from contextlib import asynccontextmanager
import logging
import sys
import traceback
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, Depends, Query, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, Base, get_db, SessionLocal, init_db, check_db_connection, sanitize_db_log
import app.models  # Ensures all SQLAlchemy models are registered

logger = logging.getLogger("uvicorn.error")

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Serverless-safe application lifespan.
    Initializes database schema cleanly without crashing module import or cold starts.
    """
    try:
        init_db()
    except Exception as e:
        logger.warning(f"Lifespan DB initialization notice: {e}")
    yield

app = FastAPI(
    title="CodeOrbit API",
    description="Backend REST API for CodeOrbit - AI Personalized Learning Platform for Engineering Students",
    version="1.0.0",
    lifespan=lifespan
)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    exc_type = type(exc).__name__
    clean_msg = sanitize_db_log(str(exc))
    clean_tb = sanitize_db_log(traceback.format_exc())
    sys.stderr.write(f"\n[UNHANDLED EXCEPTION on {request.method} {request.url.path}] {exc_type}: {clean_msg}\n")
    sys.stderr.write(f"{clean_tb}\n\n")
    sys.stderr.flush()
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error_type": exc_type,
            "detail": f"Internal error during request ({exc_type}): {clean_msg}",
            "path": request.url.path
        }
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

@app.get("/health")
@app.get("/api/health")
def health_check():
    """Safe diagnostic endpoint reporting health status without exposing sensitive credentials."""
    db_check = check_db_connection()
    is_healthy = db_check.get("database") == "connected" or db_check.get("status") == "connected"
    res = {
        "status": "healthy" if is_healthy else "degraded",
        "service": "CodeOrbit API",
        "database": "connected" if is_healthy else "disconnected",
        "dialect": db_check.get("dialect", "unknown")
    }
    if not is_healthy and "detail" in db_check:
        res["detail"] = db_check["detail"]
    return res

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
