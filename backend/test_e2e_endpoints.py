import requests

BASE_URL = "http://localhost:5173/api"

def test_full_flow():
    print("1. Testing Login...")
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "demo@codeorbit.local",
        "password": "Demo@123"
    })
    assert res.status_code == 200, f"Login failed: {res.text}"
    data = res.json()
    token = data["access_token"]
    user = data["user"]
    print(f"   Logged in successfully: {user['full_name']} | Streak: {user['streak']['current_streak']}d | Level: {user['level']} | XP: {user['xp']}")

    headers = {"Authorization": f"Bearer {token}"}

    print("\n2. Testing Subjects...")
    res = requests.get(f"{BASE_URL}/subjects", headers=headers)
    assert res.status_code == 200
    subjects = res.json()
    print(f"   Retrieved {len(subjects)} subjects: {[s['slug'] for s in subjects]}")

    print("\n3. Testing Recommendations...")
    res = requests.get(f"{BASE_URL}/recommendations", headers=headers)
    assert res.status_code == 200
    recs = res.json()
    print(f"   Retrieved recommendations: Focus: {recs['primary_focus']['topic_title'] if recs.get('primary_focus') else 'None'}")

    print("\n4. Testing AI Tutor Question...")
    res = requests.post(f"{BASE_URL}/ai/chat", headers=headers, json={
        "message": "Explain B+ Trees in DBMS"
    })
    if res.status_code != 200:
        print("AI Tutor Error:", res.status_code, res.text)
    assert res.status_code == 200
    ai_resp = res.json()
    print(f"   AI Response length: {len(ai_resp['message'])} chars")
    if ai_resp.get("quick_check"):
        print(f"   Quick check question: {ai_resp['quick_check']['question']}")

    print("\n5. Testing Placement Hub...")
    res = requests.get(f"{BASE_URL}/career/questions", headers=headers)
    assert res.status_code == 200
    print(f"   Career questions count: {len(res.json())}")

    res = requests.get(f"{BASE_URL}/career/companies", headers=headers)
    assert res.status_code == 200
    print(f"   Company guides count: {len(res.json())}")

    print("\n6. Testing Study Planner...")
    res = requests.get(f"{BASE_URL}/planner", headers=headers)
    assert res.status_code == 200
    print(f"   Study plan count: {len(res.json())}")

    print("\n7. Testing Notes...")
    res = requests.get(f"{BASE_URL}/notes", headers=headers)
    assert res.status_code == 200
    print(f"   Notes count: {len(res.json())}")

    print("\n8. Testing Quests & Challenges & Achievements...")
    r1 = requests.get(f"{BASE_URL}/quests/today", headers=headers)
    r2 = requests.get(f"{BASE_URL}/challenges", headers=headers)
    r3 = requests.get(f"{BASE_URL}/achievements", headers=headers)
    assert r1.status_code == 200 and r2.status_code == 200 and r3.status_code == 200
    print(f"   Quests: {len(r1.json())} | Challenges: {len(r2.json())} | Achievements: {len(r3.json())}")

    print("\nALL END-TO-END FLOW TESTS PASSED VIA VITE PROXY!")

if __name__ == "__main__":
    test_full_flow()
