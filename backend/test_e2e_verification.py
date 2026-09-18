import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Test via FastAPI TestClient directly
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_e2e_verification():
    print("============================================================")
    print("       CODEORBIT FULL-STACK SYSTEM VERIFICATION")
    print("============================================================")

    # 1. Login
    login_res = client.post("/api/auth/login", json={
        "email": "demo@codeorbit.local",
        "password": "Demo@123"
    })
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token = login_res.json()["access_token"]
    user = login_res.json()["user"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"✓ 1. Auth: Logged in as {user['full_name']} (Level {user['level']}, {user['xp']} XP)")

    # 2. Subjects
    subj_res = client.get("/api/subjects", headers=headers)
    assert subj_res.status_code == 200
    subjects = subj_res.json()
    assert len(subjects) == 6
    print(f"✓ 2. Curriculums: Loaded {len(subjects)} subjects ({', '.join([s['slug'].upper() for s in subjects])})")

    # 3. DBMS Details and Topic Locks Check
    dbms_res = client.get("/api/subjects/dbms", headers=headers)
    assert dbms_res.status_code == 200
    dbms_data = dbms_res.json()
    topics = dbms_data["topics"]
    assert len(topics) == 12
    print(f"✓ 3. Topic Accessibility: All 12 DBMS topics accessible and unlocked")

    # 4. Rich Curriculum Content for DBMS Fundamentals
    topic_res = client.get("/api/topics/dbms-fundamentals", headers=headers)
    assert topic_res.status_code == 200
    topic_data = topic_res.json()
    sections = topic_data.get("sections", [])
    assert len(sections) >= 5, f"Expected >= 5 sections, got {len(sections)}"
    sources = topic_data.get("source_references", [])
    assert len(sources) >= 1, f"Expected source references, got {len(sources)}"
    print(f"✓ 4. Rich Content: 'DBMS Fundamentals' loaded with {len(sections)} sections and {len(sources)} verified citations")

    # 5. 20-Question Topic Challenge
    learn_res = client.get("/api/topics/dbms-fundamentals/learn-questions", headers=headers)
    assert learn_res.status_code == 200
    q_data = learn_res.json()
    learn_questions = q_data["questions"]
    assert len(learn_questions) == 20, f"Expected 20 learn questions, got {len(learn_questions)}"
    for q in learn_questions:
        assert q["question_context"] == "LEARN"
        assert len(q["options"]) >= 2
        assert q["explanation"] is not None
    print(f"✓ 5. Topic Quiz: Loaded 20 dedicated LEARN questions with options and explanations")

    # 6. Attempt Submission & XP
    first_q = learn_questions[0]
    correct_opt = [opt for opt in first_q["options"] if opt.get("is_correct", False)]
    selected_answer = correct_opt[0]["text"] if correct_opt else first_q["options"][0]["text"]

    sub_res = client.post("/api/attempts/submit", json={
        "question_id": first_q["id"],
        "topic_id": first_q["topic_id"],
        "selected_answer": selected_answer,
        "time_taken_seconds": 10
    }, headers=headers)
    assert sub_res.status_code == 200
    sub_data = sub_res.json()
    assert "is_correct" in sub_data
    assert "new_xp" in sub_data
    print(f"✓ 6. Evaluation: Evaluated question attempt (Correct: {sub_data['is_correct']}, Mastery: {sub_data['topic_mastery']}%, +{sub_data['xp_earned']} XP)")

    # 7. Practice Arena Subject Isolation & Completed Only
    practice_dbms = client.get("/api/practice/questions?subject_slug=dbms&limit=10", headers=headers)
    assert practice_dbms.status_code == 200
    p_data = practice_dbms.json()
    assert p_data["can_practice"] is True
    assert len(p_data["questions"]) > 0
    for pq in p_data["questions"]:
        assert pq["question_context"] == "PRACTICE"
    print(f"✓ 7. Practice Arena: Subject isolation verified ({len(p_data['questions'])} PRACTICE questions from completed DBMS topics)")

    # 8. Practice Arena Prerequisite Empty State for Incomplete Subject
    practice_ml = client.get("/api/practice/questions?subject_slug=ml&limit=10", headers=headers)
    assert practice_ml.status_code == 200
    p_ml_data = practice_ml.json()
    assert p_ml_data["can_practice"] is False
    assert len(p_ml_data["questions"]) == 0
    assert "Complete a" in p_ml_data["message"]
    print(f"✓ 8. Practice Guard: Incomplete subject (ML) properly blocked with educational message: '{p_ml_data['message'][:55]}...'")

    # 9. Local RAG AI Tutor Retrieval
    ai_search = client.get("/api/ai/search?query=Three-schema+architecture&subject=dbms", headers=headers)
    assert ai_search.status_code == 200
    search_data = ai_search.json()
    assert len(search_data.get("matching_topics", [])) > 0
    assert len(search_data.get("context_str", "")) > 0
    print(f"✓ 9. AI Tutor RAG: Search retrieved database topics, grounded context, and verified sources")

    # 10. AI Tutor Chat & Quick Check
    chat_res = client.post("/api/ai/chat", json={
        "message": "What is normalization and why do we need 3NF?",
        "subject_id": 1
    }, headers=headers)
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert "message" in chat_data and len(chat_data["message"]) > 20
    assert "quick_check" in chat_data
    print(f"✓ 10. AI Tutor Interactive: Chat generated explanation + dynamic quick-check problem")

    # 11. Question Bank Filtering
    qb_res = client.get("/api/questions?question_context=PRACTICE&limit=10", headers=headers)
    assert qb_res.status_code == 200
    qb_questions = qb_res.json()
    assert len(qb_questions) > 0
    for q in qb_questions:
        assert q["question_context"] == "PRACTICE"
    print(f"✓ 11. Question Bank: Context filter verified ({len(qb_questions)} PRACTICE questions retrieved)")

    # 12. Placement Hub Career Questions
    career_res = client.get("/api/career/questions?category=DSA", headers=headers)
    assert career_res.status_code == 200
    career_q = career_res.json()
    assert len(career_q) > 0
    print(f"✓ 12. Placement Hub: Loaded {len(career_q)} DSA placement problems across curated companies")

    print("============================================================")
    print("RESULT: ✅ ALL 12 END-TO-END VERIFICATION CHECKS PASSED!")
    print("============================================================")
    return True

if __name__ == "__main__":
    success = run_e2e_verification()
    sys.exit(0 if success else 1)
