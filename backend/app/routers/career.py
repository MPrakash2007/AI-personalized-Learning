from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.models.career import CareerQuestion, InterviewAttempt
from app.schemas.career import (
    CareerQuestionResponse, InterviewSubmitRequest, InterviewFeedbackResponse, CompanyGuide
)
from app.auth.deps import get_current_user
from app.services.ai_service import get_ai_provider
from app.services.gamification_service import award_xp

router = APIRouter(prefix="/career", tags=["Career & Placement Hub"])

@router.get("/questions", response_model=List[CareerQuestionResponse])
def get_career_questions(
    category: Optional[str] = None,
    sub_topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(CareerQuestion)
    if category:
        query = query.filter(CareerQuestion.category == category)
    if sub_topic:
        query = query.filter(CareerQuestion.sub_topic.ilike(f"%{sub_topic}%"))
    if difficulty:
        query = query.filter(CareerQuestion.difficulty == difficulty.upper())

    return query.all()

@router.post("/interview/review", response_model=InterviewFeedbackResponse)
def submit_interview_answer(
    req: InterviewSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = get_ai_provider()
    feedback = provider.review_interview_answer(req.question_prompt, req.student_answer)

    # Save attempt in database
    attempt = InterviewAttempt(
        user_id=current_user.id,
        career_question_id=req.career_question_id,
        question_prompt=req.question_prompt,
        student_answer=req.student_answer,
        feedback_clarity=feedback["feedback_clarity"],
        feedback_depth=feedback["feedback_depth"],
        feedback_structure=feedback["feedback_structure"],
        feedback_missing=feedback["feedback_missing"],
        feedback_suggestions=feedback["feedback_suggestions"],
        overall_score=feedback["overall_score"]
    )
    db.add(attempt)
    db.commit()

    # Award interview practice XP (+25 XP)
    award_xp(db, current_user, 25, "Completed AI Interview Practice")

    return InterviewFeedbackResponse(
        overall_score=feedback["overall_score"],
        feedback_clarity=feedback["feedback_clarity"],
        feedback_depth=feedback["feedback_depth"],
        feedback_structure=feedback["feedback_structure"],
        feedback_missing=feedback["feedback_missing"],
        feedback_suggestions=feedback["feedback_suggestions"],
        xp_earned=25
    )

@router.get("/companies", response_model=List[CompanyGuide])
def get_company_guides():
    return [
        CompanyGuide(
            category_id="product",
            name="Tier-1 Product Companies",
            description="Focuses on algorithmic mastery, high-performance systems, scalability, and clean modular code.",
            target_roles=["Software Engineer (SDE I)", "Systems Engineer", "Backend Developer"],
            key_subjects=["Data Structures & Algorithms", "Operating Systems", "System Design", "DBMS"],
            common_dsa_topics=["Dynamic Programming", "Trees & Graphs", "Tries", "Sliding Window", "Heap & Priority Queues"],
            rounds_breakdown=[
                "Online Assessment: 2-3 Medium/Hard LeetCode problems",
                "Technical Round 1: DSA + Space/Time optimization",
                "Technical Round 2: Core CS (OS, Concurrency, DBMS, Networks)",
                "Managerial / Bar Raiser: System Design + STAR Behavioral"
            ],
            checklist=[
                "Solve 250+ standard DSA problems",
                "Understand ACID, Indexing, and Normalization deeply",
                "Master Threading, Locks, and Virtual Memory",
                "Prepare 3 project deep-dives using STAR framework"
            ]
        ),
        CompanyGuide(
            category_id="service",
            name="Mass Tech & IT Services",
            description="Focuses on foundational technical acumen, verbal/logical aptitude, and practical web/software development concepts.",
            target_roles=["Associate Software Engineer", "Systems Analyst", "Graduate Trainee"],
            key_subjects=["OOPS Concepts", "SQL Basics", "Networking Fundamentals", "General Aptitude"],
            common_dsa_topics=["Arrays", "Strings", "Sorting Algorithms", "Linear Search & Binary Search", "Linked Lists"],
            rounds_breakdown=[
                "Aptitude & Coding Round: Quant, Verbal, Logical + 2 coding questions",
                "Technical Interview: OOPS in Java/C++, SQL queries, project walkthrough",
                "HR Interview: Communication skills, relocation, teamwork"
            ],
            checklist=[
                "Practice speed-solving for aptitude questions",
                "Be ready to write clean SQL Joins and Aggregations on a whiteboard",
                "Explain the 4 pillars of OOP with real-world code examples",
                "Polished resume highlighting academic projects"
            ]
        ),
        CompanyGuide(
            category_id="fintech",
            name="FinTech & Quant Firms",
            description="Requires extreme precision, micro-latency awareness, database transaction guarantees, and strong math/logic.",
            target_roles=["Fintech Software Engineer", "Platform Engineer", "Quant Developer"],
            key_subjects=["Transactions & Concurrency", "Low-level OS & Networking", "High-frequency DSA", "Distributed Systems"],
            common_dsa_topics=["Segment Trees", "Bit Manipulation", "Concurrent Queues", "Graph Shortest Paths"],
            rounds_breakdown=[
                "Rigorous Online Test: Advanced Algorithms + Math/Puzzles",
                "Technical Interview 1: Data structures with concurrency safety",
                "Technical Interview 2: Low-level architecture & DB isolation levels",
                "Final Culture & Architecture Interview"
            ],
            checklist=[
                "Master Transaction Isolation Levels (Read Committed vs Serializable)",
                "Understand TCP packet structures and zero-copy buffers",
                "Practice multithreaded programming in C++ / Java / Go",
                "Review probability, statistics, and discrete math"
            ]
        ),
        CompanyGuide(
            category_id="startups",
            name="Fast-Paced Startups & Scaleups",
            description="Values end-to-end full-stack velocity, API design, modern frameworks, and rapid problem-solving.",
            target_roles=["Full-Stack Engineer", "Frontend / Backend Specialist", "Product Engineer"],
            key_subjects=["REST / GraphQL APIs", "Frontend Architecture", "Database Schema Design", "Git & CI/CD"],
            common_dsa_topics=["Hash Maps", "Two Pointers", "BFS/DFS", "Array Manipulations"],
            rounds_breakdown=[
                "Take-home Assignment or Live Coding Session",
                "Code Review & Architecture Discussion of your project",
                "Founder / Engineering Lead Culture Fit Round"
            ],
            checklist=[
                "Have 2 production-grade deployed web projects on GitHub",
                "Demonstrate clean Git commit discipline and PR workflows",
                "Explain how you handle async state, JWT auth, and database migrations",
                "Show high ownership and product intuition"
            ]
        )
    ]
