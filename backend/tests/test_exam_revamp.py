"""
Comprehensive Integration Tests for CodeOrbit Exam-Oriented Learning Revamp
Tests:
1. All 6 subjects & 74 topics accessible
2. 12 structured exam sections per topic
3. Sequential progression: Topic 1 AVAILABLE -> Quiz complete -> Topic 2 unlocked
4. Quick Reference endpoint integrity for all sections
5. 403 guard on locked topic questions
6. AI Tutor grounded retrieval in 7-part exam layout
7. Practice Arena completed topic restrictions
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models.user import User
from app.models.learning import Subject, Topic, TopicProgress
from app.auth.security import hash_password

client = TestClient(app)

@pytest.fixture(scope="module")
def auth_headers():
    # Login as demo user
    login_res = client.post("/api/auth/login", json={
        "email": "demo@codeorbit.local",
        "password": "Demo@123"
    })
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def fresh_user_headers():
    import uuid
    email = f"student_{uuid.uuid4().hex[:8]}@codeorbit.local"
    reg_res = client.post("/api/auth/register", json={
        "email": email,
        "password": "Password@123",
        "confirm_password": "Password@123",
        "full_name": "Progression Test Student",
        "college": "Tech University",
        "branch": "Computer Science"
    })
    assert reg_res.status_code == 200
    token = reg_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_all_six_subjects_and_topics(auth_headers):
    res = client.get("/api/subjects", headers=auth_headers)
    assert res.status_code == 200
    subjects = res.json()
    assert len(subjects) == 6
    expected_slugs = {"dbms", "oops", "os", "ds", "ml", "cn"}
    assert {s["slug"] for s in subjects} == expected_slugs

    total_topics = sum(s["topics_count"] for s in subjects)
    assert total_topics == 74


def test_quick_reference_endpoint(auth_headers):
    # Test DBMS Fundamentals Quick Reference
    res = client.get("/api/topics/dbms-fundamentals/quick-reference", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()

    assert data["topic_slug"] == "dbms-fundamentals"
    assert "DBMS" in data["title"] or "Fundamentals" in data["title"]
    assert len(data["exam_definition"]) > 20
    assert len(data["key_points"]) >= 3
    assert data["how_it_works"] is not None
    assert data["comparison"] is not None
    assert len(data["formulas"]) >= 1
    assert data["exam_tip"] is not None
    assert data["common_confusion"] is not None
    assert len(data["faqs"]) >= 3
    assert len(data["revision_60s"]) >= 3
    assert len(data["references"]) >= 2

    # Verify that URLs are real and non-synthetic
    for ref in data["references"]:
        assert "geeksforgeeks.org" in ref["source_url"] or "tutorialspoint.com" in ref["source_url"]
        assert "/dbms-fundamentals/" not in ref["source_url"]


def test_topic_twelve_sections(auth_headers):
    # Verify DBMS Fundamentals has 12 compiled sections
    res = client.get("/api/topics/dbms-fundamentals", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()

    sections = data["sections"]
    assert len(sections) == 12
    expected_types = [
        "exam_definition", "core_concept", "key_points", "classification",
        "how_it_works", "example", "comparison", "formula",
        "exam_tip", "common_confusion", "important_questions", "revision_60s"
    ]
    actual_types = [s["section_type"] for s in sections]
    assert actual_types == expected_types


def test_fresh_user_sequential_progression(fresh_user_headers):
    # Check OOPS subject roadmap for fresh user
    res = client.get("/api/subjects/oops", headers=fresh_user_headers)
    assert res.status_code == 200
    data = res.json()
    topics = data["topics"]
    assert len(topics) == 11

    # Topic 1 (oop-fundamentals) must be AVAILABLE
    t1 = topics[0]
    assert t1["slug"] == "oop-fundamentals"
    assert t1["is_accessible"] is True
    assert t1["status"] == "AVAILABLE"

    # Topic 2 (classes-and-objects) must be UPCOMING and NOT accessible
    t2 = topics[1]
    assert t2["slug"] == "classes-and-objects"
    assert t2["is_accessible"] is False
    assert t2["status"] == "UPCOMING"

    # Trying to load Learn questions for locked Topic 2 must return 403 Forbidden
    locked_q_res = client.get(f"/api/topics/{t2['slug']}/learn-questions", headers=fresh_user_headers)
    assert locked_q_res.status_code == 403

    # Load questions for Topic 1 (must succeed)
    t1_q_res = client.get(f"/api/topics/{t1['slug']}/learn-questions", headers=fresh_user_headers)
    assert t1_q_res.status_code == 200
    questions = t1_q_res.json()["questions"]
    assert len(questions) >= 15

    # Submit Topic 1 Quiz to complete and unlock Topic 2
    answers = [
        {"question_id": q["id"], "is_correct": True, "time_taken_seconds": 10}
        for q in questions
    ]
    complete_res = client.post(
        f"/api/topics/{t1['slug']}/complete-quiz",
        json={"answers": answers, "time_taken_seconds": 150},
        headers=fresh_user_headers
    )
    assert complete_res.status_code == 200
    c_data = complete_res.json()
    assert c_data["status"] in ["COMPLETED", "MASTERED"]
    assert c_data["next_topic_slug"] == "classes-and-objects"
    assert c_data["xp_awarded"] > 0

    # Verify that Topic 2 is now unlocked and accessible!
    res_after = client.get("/api/subjects/oops", headers=fresh_user_headers)
    topics_after = res_after.json()["topics"]
    t1_after = topics_after[0]
    t2_after = topics_after[1]

    # Topic 1 remains completed & accessible (COMPLETED != LOCKED)
    assert t1_after["is_completed"] is True
    assert t1_after["is_accessible"] is True
    assert t1_after["status"] in ["COMPLETED", "MASTERED"]

    # Topic 2 is now AVAILABLE & accessible
    assert t2_after["is_accessible"] is True
    assert t2_after["status"] == "AVAILABLE"

    # Now questions for Topic 2 can be fetched
    t2_q_res = client.get(f"/api/topics/{t2['slug']}/learn-questions", headers=fresh_user_headers)
    assert t2_q_res.status_code == 200


def test_ai_tutor_grounded_exam_format(auth_headers):
    # Query AI tutor on a core syllabus topic
    res = client.post("/api/ai/chat", json={
        "message": "Explain BCNF and why dependency preservation can be violated."
    }, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()

    reply = data["message"]
    # Check that it contains exam breakdown headers
    assert "Exam Prep Breakdown" in reply or "Concept Definition" in reply
    assert "Key" in reply
    assert "References" in reply

    # Check zero generic filler phrases
    assert "indispensable core concept" not in reply.lower()
    assert "engineering bottleneck" not in reply.lower()
    assert "underlying runtime" not in reply.lower()

    # Check quick check question
    assert data["quick_check"] is not None
    assert len(data["sources"]) > 0


def test_practice_arena_restriction(fresh_user_headers):
    # Fresh user has 0 completed topics in OS
    res = client.get("/api/practice/questions?subject_slug=os&limit=10", headers=fresh_user_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["can_practice"] is False
    assert len(data["questions"]) == 0
    assert "Complete a" in data["message"]
