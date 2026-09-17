import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models.user import User

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "CodeOrbit"
    assert data["status"] == "online"

def test_login_demo_user():
    response = client.post("/api/auth/login", json={
        "email": "demo@codeorbit.local",
        "password": "Demo@123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "demo@codeorbit.local"
    assert data["user"]["level"] >= 1
    assert data["user"]["xp"] >= 2000

def test_get_subjects():
    # Login first
    login_res = client.post("/api/auth/login", json={
        "email": "demo@codeorbit.local",
        "password": "Demo@123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/subjects", headers=headers)
    assert response.status_code == 200
    subjects = response.json()
    assert len(subjects) == 6
    names = [s["name"] for s in subjects]
    assert "DBMS" in names
    assert "OOPS" in names
    assert "OS" in names
    assert "DS" in names
    assert "ML" in names
    assert "CN" in names

def test_get_subject_details():
    login_res = client.post("/api/auth/login", json={
        "email": "demo@codeorbit.local",
        "password": "Demo@123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/subjects/dbms", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "DBMS"
    assert len(data["topics"]) == 12

def test_attempt_submission_and_xp():
    login_res = client.post("/api/auth/login", json={
        "email": "demo@codeorbit.local",
        "password": "Demo@123"
    })
    token = login_res.json()["access_token"]
    user_id = login_res.json()["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch a question from questions endpoint
    q_res = client.get("/api/questions?limit=1", headers=headers)
    assert q_res.status_code == 200
    questions = q_res.json()
    assert len(questions) > 0
    test_q = questions[0]

    # Submit an attempt
    attempt_res = client.post("/api/attempts/submit", json={
        "question_id": test_q["id"],
        "topic_id": test_q["topic_id"],
        "selected_answer": test_q["options"][0]["text"] if test_q["options"] else "test",
        "time_taken_seconds": 15
    }, headers=headers)
    assert attempt_res.status_code == 200
    res_data = attempt_res.json()
    assert "is_correct" in res_data
    assert "new_xp" in res_data
    assert "topic_mastery" in res_data
    assert "current_streak" in res_data

def test_ai_tutor_and_explain_mistake():
    login_res = client.post("/api/auth/login", json={
        "email": "demo@codeorbit.local",
        "password": "Demo@123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    chat_res = client.post("/api/ai/chat", json={
        "message": "What is normalization and why do we need 3NF?"
    }, headers=headers)
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert "message" in chat_data
    assert len(chat_data["message"]) > 20
    assert "quick_check" in chat_data

def test_progress_overview():
    login_res = client.post("/api/auth/login", json={
        "email": "demo@codeorbit.local",
        "password": "Demo@123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    prog_res = client.get("/api/progress/overview", headers=headers)
    assert prog_res.status_code == 200
    pdata = prog_res.json()
    assert "total_xp" in pdata
    assert "overall_mastery" in pdata
    assert len(pdata["subject_mastery"]) == 6

def test_career_questions_and_companies():
    login_res = client.post("/api/auth/login", json={
        "email": "demo@codeorbit.local",
        "password": "Demo@123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    cq_res = client.get("/api/career/questions", headers=headers)
    assert cq_res.status_code == 200
    assert len(cq_res.json()) > 0

    comp_res = client.get("/api/career/companies", headers=headers)
    assert comp_res.status_code == 200
    assert len(comp_res.json()) >= 4
