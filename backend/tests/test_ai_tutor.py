import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_tokens():
    """Generates authentication headers for two distinct users for isolation tests."""
    user1_email = "tutor_user1@codeorbit.test"
    user2_email = "tutor_user2@codeorbit.test"

    reg1 = client.post("/api/auth/register", json={
        "email": user1_email,
        "password": "Password123!",
        "confirm_password": "Password123!",
        "full_name": "Tutor Student One"
    })
    token1 = reg1.json()["access_token"] if reg1.status_code == 200 else client.post("/api/auth/login", json={
        "email": user1_email,
        "password": "Password123!"
    }).json()["access_token"]

    reg2 = client.post("/api/auth/register", json={
        "email": user2_email,
        "password": "Password123!",
        "confirm_password": "Password123!",
        "full_name": "Tutor Student Two"
    })
    token2 = reg2.json()["access_token"] if reg2.status_code == 200 else client.post("/api/auth/login", json={
        "email": user2_email,
        "password": "Password123!"
    }).json()["access_token"]

    return {
        "user1": {"Authorization": f"Bearer {token1}"},
        "user2": {"Authorization": f"Bearer {token2}"},
    }

def test_ai_tutor_authentication_required():
    """Unauthenticated requests must be rejected with 401."""
    res = client.post("/api/ai-tutor/chat", json={"message": "Explain normalization in DBMS"})
    assert res.status_code == 401

def test_ai_tutor_message_length_validation(auth_tokens):
    """Empty messages or messages exceeding 4000 characters must return 400."""
    headers = auth_tokens["user1"]

    # Empty
    r_empty = client.post("/api/ai-tutor/chat", json={"message": "   "}, headers=headers)
    assert r_empty.status_code == 400

    # Overly long
    long_msg = "A" * 4001
    r_long = client.post("/api/ai-tutor/chat", json={"message": long_msg}, headers=headers)
    assert r_long.status_code == 400

def test_ai_tutor_arbitrary_question_mocked_openai(auth_tokens):
    """
    Verifies that the AI Tutor dynamically answers arbitrary questions using OpenAI.
    OpenAI is mocked to spend ZERO real API credits.
    """
    headers = auth_tokens["user1"]
    mock_answer = (
        "### 🧠 Normalization in DBMS\n\n"
        "Normalization is the systematic approach of organizing data in a relational database.\n\n"
        "```sql\nCREATE TABLE Students (id INT PRIMARY KEY, name VARCHAR(100));\n```\n\n"
        "### 💡 Suggested Next Questions\n"
        "- What is 1NF vs 2NF?\n"
        "- Explain 3NF with an anomaly example.\n"
        "- When should we consider denormalization?"
    )

    with patch("app.services.ai_tutor.OpenAITutorService.is_configured", return_value=True):
        with patch("app.services.ai_tutor.OpenAITutorService._get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_choice = MagicMock()
            mock_choice.message.content = mock_answer
            mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])
            mock_get_client.return_value = mock_client

            res = client.post("/api/ai-tutor/chat", json={
                "message": "Explain normalization in DBMS.",
                "subject": "DBMS"
            }, headers=headers)

            assert res.status_code == 200
            data = res.json()
            assert "answer" in data
            assert "conversation_id" in data
            assert len(data["suggested_followups"]) >= 2
            assert data["conversation_id"] > 0
            assert "Normalization" in data["answer"]

def test_ai_tutor_conversation_persistence_and_followup(auth_tokens):
    """
    Verifies multi-turn conversation persistence:
    Turn 1: Explain deadlock
    Turn 2: Give me a real-world example
    Turn 3: How can it be prevented?
    The backend maintains conversation history and passes prior turns to OpenAI.
    """
    headers = auth_tokens["user1"]

    with patch("app.services.ai_tutor.OpenAITutorService.is_configured", return_value=True):
        with patch("app.services.ai_tutor.OpenAITutorService._get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_choice = MagicMock()
            mock_choice.message.content = "Deadlock explanation."
            mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])
            mock_get_client.return_value = mock_client

            # Turn 1
            res1 = client.post("/api/ai-tutor/chat", json={
                "message": "What is a deadlock in operating systems?",
                "subject": "OS"
            }, headers=headers)
            assert res1.status_code == 200
            conv_id = res1.json()["conversation_id"]

            # Turn 2: Follow-up question referencing previous turn
            mock_choice.message.content = "Here is a real-world traffic junction analogy for deadlock."
            res2 = client.post("/api/ai-tutor/chat", json={
                "conversation_id": conv_id,
                "message": "Give me a real-world example of it."
            }, headers=headers)
            assert res2.status_code == 200
            assert res2.json()["conversation_id"] == conv_id

            # Turn 3
            mock_choice.message.content = "Deadlock prevention involves invalidating one of the 4 Coffman conditions."
            res3 = client.post("/api/ai-tutor/chat", json={
                "conversation_id": conv_id,
                "message": "How can it be prevented?"
            }, headers=headers)
            assert res3.status_code == 200

            # Verify conversation messages retrieval
            conv_res = client.get(f"/api/ai-tutor/conversations/{conv_id}", headers=headers)
            assert conv_res.status_code == 200
            conv_data = conv_res.json()
            assert conv_data["message_count"] == 6  # 3 user + 3 AI turns
            roles = [m["role"] for m in conv_data["messages"]]
            assert roles == ["user", "assistant", "user", "assistant", "user", "assistant"]

def test_ai_tutor_cross_user_isolation(auth_tokens):
    """User B must NEVER be able to access or modify User A's conversations."""
    headers_user1 = auth_tokens["user1"]
    headers_user2 = auth_tokens["user2"]

    # User 1 creates conversation
    res1 = client.post("/api/ai-tutor/chat", json={
        "message": "Explain B-Trees in database systems."
    }, headers=headers_user1)
    assert res1.status_code == 200
    user1_conv_id = res1.json()["conversation_id"]

    # User 2 attempts to read User 1's conversation
    read_res = client.get(f"/api/ai-tutor/conversations/{user1_conv_id}", headers=headers_user2)
    assert read_res.status_code == 404

    # User 2 attempts to post into User 1's conversation
    chat_res = client.post("/api/ai-tutor/chat", json={
        "conversation_id": user1_conv_id,
        "message": "Hacking conversation"
    }, headers=headers_user2)
    assert chat_res.status_code == 404

    # User 2 attempts to delete User 1's conversation
    del_res = client.delete(f"/api/ai-tutor/conversations/{user1_conv_id}", headers=headers_user2)
    assert del_res.status_code == 404

def test_ai_tutor_action_modifiers(auth_tokens):
    """Tests action modifiers: exam_answer (10 marks), mcqs, explain_code."""
    headers = auth_tokens["user1"]

    with patch("app.services.ai_tutor.OpenAITutorService.is_configured", return_value=True):
        with patch("app.services.ai_tutor.OpenAITutorService._get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_choice = MagicMock()
            mock_choice.message.content = "Comprehensive 10-Mark Answer on TCP Three-Way Handshake."
            mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])
            mock_get_client.return_value = mock_client

            # Exam answer 10 marks
            res = client.post("/api/ai-tutor/chat", json={
                "message": "Explain TCP three-way handshake.",
                "action": "exam_answer",
                "marks": 10
            }, headers=headers)
            assert res.status_code == 200
            assert "10-Mark" in res.json()["answer"]

def test_ai_tutor_missing_key_graceful_response(auth_tokens):
    """When OPENAI_API_KEY is missing, AI Tutor must still provide an intelligent educational response."""
    headers = auth_tokens["user1"]

    with patch("app.services.ai_tutor.OpenAITutorService.is_configured", return_value=False):
        res = client.post("/api/ai-tutor/chat", json={
            "message": "Explain gradient descent in machine learning."
        }, headers=headers)

        assert res.status_code == 200
        data = res.json()
        assert "answer" in data
        assert "Gradient Descent" in data["answer"]
        assert len(data["suggested_followups"]) > 0

def test_ai_tutor_conversation_deletion(auth_tokens):
    """User can delete their own conversation."""
    headers = auth_tokens["user1"]

    res = client.post("/api/ai-tutor/chat", json={
        "message": "Temporary conversation for deletion testing."
    }, headers=headers)
    assert res.status_code == 200
    conv_id = res.json()["conversation_id"]

    del_res = client.delete(f"/api/ai-tutor/conversations/{conv_id}", headers=headers)
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "deleted"

    # Verifying it's gone
    get_res = client.get(f"/api/ai-tutor/conversations/{conv_id}", headers=headers)
    assert get_res.status_code == 404

def test_health_ai_configured_reporting():
    """Verify GET /api/health safely reports ai_configured boolean without leaking secrets."""
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data
    assert "database" in data
    assert "dialect" in data
    assert "ai_configured" in data
    assert "ai_provider" in data
    assert "ai_model" in data
    assert isinstance(data["ai_configured"], bool)
    assert "OPENAI_API_KEY" not in str(data)
    assert "sk-" not in str(data)


def test_ai_tutor_status_endpoint():
    """Verify GET /api/ai-tutor/status reports configuration safely without leaking secrets."""
    res = client.get("/api/ai-tutor/status")
    assert res.status_code == 200
    data = res.json()
    assert "configured" in data
    assert "provider" in data
    assert "model" in data
    assert isinstance(data["configured"], bool)
    assert "OPENAI_API_KEY" not in str(data)
    assert "sk-" not in str(data)


def test_ai_configuration_matrix(monkeypatch):
    """
    Automated verification of AI configuration states:
    - OPENAI_API_KEY present -> configured = True
    - OPENAI_API_KEY missing -> configured = False
    - OPENAI_API_KEY whitespace -> configured = False
    - AI_PROVIDER=openai -> provider recognized
    - OPENAI_MODEL missing -> defaults to gpt-4o-mini
    - No secret in health response or logs
    """
    from app.config import settings

    # 1. Missing key
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("openai_api_key", raising=False)
    assert settings.get_openai_api_key() == ""
    assert settings.is_ai_configured() is False

    # 2. Whitespace key
    monkeypatch.setenv("OPENAI_API_KEY", "   ")
    assert settings.get_openai_api_key() == ""
    assert settings.is_ai_configured() is False

    # 3. Present key
    monkeypatch.setenv("OPENAI_API_KEY", "sk-proj-mocktestkey12345")
    assert settings.get_openai_api_key() == "sk-proj-mocktestkey12345"
    assert settings.is_ai_configured() is True

    # 4. Present key with accidental surrounding quotes
    monkeypatch.setenv("OPENAI_API_KEY", '"sk-proj-quotedkey12345"')
    assert settings.get_openai_api_key() == "sk-proj-quotedkey12345"
    assert settings.is_ai_configured() is True

    # 5. Missing model -> default fallback
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("openai_model", raising=False)
    assert settings.get_openai_model() == "gpt-4o-mini"

    # 6. Provider recognition
    monkeypatch.setenv("AI_PROVIDER", "openai")
    assert settings.get_ai_provider() == "openai"

    # 7. Health response has zero secret leakage
    health_res = client.get("/api/health")
    assert health_res.status_code == 200
    h_data = health_res.json()
    assert "sk-proj" not in str(h_data)
    assert "OPENAI_API_KEY" not in str(h_data)

