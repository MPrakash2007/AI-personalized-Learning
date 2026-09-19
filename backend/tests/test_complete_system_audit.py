import os
import sys
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_public_endpoints():
    """Verify public endpoints return expected structure."""
    r = client.get("/api")
    assert r.status_code == 200
    assert r.json()["status"] == "online"

    health = client.get("/api/health")
    assert health.status_code == 200
    assert "status" in health.json()
    assert "service" in health.json()
    assert "database" in health.json()


def test_complete_auth_lifecycle():
    """Verify registration, login, and authenticated me endpoint."""
    unique_email = f"audit_user_{os.getpid()}@codeorbit.test"
    payload = {
        "email": unique_email,
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!",
        "full_name": "Audit Student",
        "college": "National Institute of Tech",
        "degree": "B.Tech",
        "branch": "CSE",
        "graduation_year": 2026
    }

    # 1. Register
    reg_res = client.post("/api/auth/register", json=payload)
    assert reg_res.status_code == 200, f"Register failed: {reg_res.text}"
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == unique_email
    assert reg_data["user"]["streak"]["current_streak"] == 0

    # 2. Duplicate registration should return 400
    dup_res = client.post("/api/auth/register", json=payload)
    assert dup_res.status_code == 400

    # 3. Login
    login_res = client.post("/api/auth/login", json={"email": unique_email, "password": "StrongPassword123!"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    assert token

    # 4. Authenticated /me
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == unique_email


def test_curriculum_and_subjects_structure():
    """Verify all 6 core subjects are exposed with structured curriculum."""
    unique_email = f"audit_curriculum_{os.getpid()}@codeorbit.test"
    reg = client.post("/api/auth/register", json={
        "email": unique_email,
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!",
        "full_name": "Curriculum Verifier"
    })
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Verify Subjects
    sub_res = client.get("/api/subjects", headers=headers)
    assert sub_res.status_code == 200
    subjects = sub_res.json()
    assert len(subjects) >= 6
    slugs = {s["slug"] for s in subjects}
    expected_slugs = {"dbms", "oops", "os", "ds", "ml", "cn"}
    assert expected_slugs.issubset(slugs)

    # Verify Topic Quick Reference
    qr_res = client.get("/api/topics/dbms-fundamentals/quick-reference", headers=headers)
    assert qr_res.status_code == 200
    qr_data = qr_res.json()
    assert qr_data["topic_slug"] == "dbms-fundamentals"
    assert "exam_definition" in qr_data
    assert len(qr_data["references"]) >= 1


def test_ai_tutor_fallback_resilience():
    """Verify AI tutor responds intelligently even without external AI keys."""
    unique_email = f"audit_ai_{os.getpid()}@codeorbit.test"
    reg = client.post("/api/auth/register", json={
        "email": unique_email,
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!",
        "full_name": "AI Verifier"
    })
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    ai_res = client.post("/api/ai/chat", headers=headers, json={
        "message": "What is 3NF in DBMS?",
        "context": "DBMS Normalization"
    })
    assert ai_res.status_code == 200
    reply = ai_res.json().get("reply", "")
    assert len(reply) > 20
    assert "3NF" in reply or "normalization" in reply.lower() or "functional" in reply.lower()


def test_career_hub_endpoints():
    """Verify career hub company guides and interview questions."""
    unique_email = f"audit_career_{os.getpid()}@codeorbit.test"
    reg = client.post("/api/auth/register", json={
        "email": unique_email,
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!",
        "full_name": "Career Verifier"
    })
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    comp_res = client.get("/api/career/companies", headers=headers)
    assert comp_res.status_code == 200
    assert len(comp_res.json()) >= 1

    cq_res = client.get("/api/career/questions", headers=headers)
    assert cq_res.status_code == 200
    assert len(cq_res.json()) >= 1
