import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.exc import ProgrammingError, OperationalError
from app.main import app
from app.models.user import User, UserPreferences, LearningStreak
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token

client = TestClient(app)

def test_password_hashing_and_verification():
    """Verify password hashing produces bcrypt hashes and verifies accurately."""
    pwd = "MySecretPassword123!"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

import uuid

def test_login_invalid_password_returns_401():
    """Valid registered user with wrong password must return 401 Unauthorized."""
    email = f"invalid_pwd_{uuid.uuid4().hex[:8]}@codeorbit.test"
    # Register
    reg = client.post("/api/auth/register", json={
        "email": email,
        "password": "CorrectPassword123!",
        "confirm_password": "CorrectPassword123!",
        "full_name": "Test User"
    })
    assert reg.status_code == 200

    # Login with wrong password
    login_res = client.post("/api/auth/login", json={
        "email": email,
        "password": "WrongPassword123!"
    })
    assert login_res.status_code == 401
    assert "Invalid email or password" in login_res.json()["detail"]

def test_login_nonexistent_user_returns_401():
    """Nonexistent user email must return 401 Unauthorized."""
    login_res = client.post("/api/auth/login", json={
        "email": f"completely_nonexistent_{uuid.uuid4().hex[:8]}@codeorbit.test",
        "password": "AnyPassword123!"
    })
    assert login_res.status_code == 401
    assert "Invalid email or password" in login_res.json()["detail"]

def test_get_me_with_valid_jwt():
    """GET /api/auth/me returns the current authenticated user's profile."""
    email = f"get_me_{uuid.uuid4().hex[:8]}@codeorbit.test"
    reg = client.post("/api/auth/register", json={
        "email": email,
        "password": "Password123!",
        "confirm_password": "Password123!",
        "full_name": "Get Me Student"
    })
    assert reg.status_code == 200
    token = reg.json()["access_token"]

    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == email
    assert data["full_name"] == "Get Me Student"
    assert "hashed_password" not in data

def test_get_me_unauthenticated_returns_401():
    """GET /api/auth/me without token or with bad token returns 401."""
    res_no_auth = client.get("/api/auth/me")
    assert res_no_auth.status_code == 401

    res_bad_token = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid.jwt.token"})
    assert res_bad_token.status_code == 401

def test_login_database_programming_error_handling():
    """
    When login encounters a PostgreSQL ProgrammingError (e.g. permission denied or missing relation),
    it must log the sanitized error and return an informative 503 instead of a generic crash.
    """
    mock_orig = MagicMock()
    mock_orig.__str__ = MagicMock(return_value="permission denied for table users")
    prog_err = ProgrammingError("SELECT * FROM users", {}, mock_orig)

    with patch("sqlalchemy.orm.Session.query") as mock_query:
        mock_query.side_effect = prog_err
        res = client.post("/api/auth/login", json={
            "email": "anyuser@codeorbit.test",
            "password": "Password123!"
        })
        assert res.status_code == 503
        data = res.json()
        assert "Database error during login" in data["detail"]
        assert "permission denied for table users" in data["detail"]

def test_get_me_database_error_handling():
    """
    When /api/auth/me encounters a database error during user lookup,
    it must return HTTP 503 rather than an unhandled 500 crash.
    """
    token = create_access_token(data={"sub": "1"})
    mock_orig = MagicMock()
    mock_orig.__str__ = MagicMock(return_value="permission denied for table users")
    prog_err = ProgrammingError("SELECT * FROM users WHERE id = 1", {}, mock_orig)

    with patch("sqlalchemy.orm.Session.query") as mock_query:
        mock_query.side_effect = prog_err
        res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 503
        assert "Database error during user authentication" in res.json()["detail"]

def test_user_model_schema_matches_expected():
    """Verify that User SQLAlchemy model defines all required columns and relationships."""
    user_cols = {c.name: c for c in User.__table__.columns}
    required_cols = [
        "id", "email", "hashed_password", "full_name", "college",
        "degree", "branch", "graduation_year", "avatar_url", "is_admin",
        "level", "xp", "gems", "onboarding_completed", "created_at", "updated_at"
    ]
    for col in required_cols:
        assert col in user_cols, f"Missing required column '{col}' in User model"

    # Check UserPreferences
    pref_cols = {c.name: c for c in UserPreferences.__table__.columns}
    assert "user_id" in pref_cols
    assert "programming_level" in pref_cols

    # Check LearningStreak
    streak_cols = {c.name: c for c in LearningStreak.__table__.columns}
    assert "user_id" in streak_cols
    assert "current_streak" in streak_cols
