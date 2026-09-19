import uuid
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models.user import User, LearningStreak, UserPreferences

client = TestClient(app)

def cleanup_test_users():
    db = SessionLocal()
    try:
        test_users = db.query(User).filter(User.email.like("test_%@codeorbit.local")).all()
        for u in test_users:
            db.delete(u)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    cleanup_test_users()
    yield
    cleanup_test_users()

def test_health_check_endpoint():
    """Verify diagnostic health check route."""
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["service"] == "CodeOrbit API"
    assert "status" in data
    assert "database" in data
    assert "dialect" in data

def test_successful_registration():
    """Verify standard valid user registration returns access_token, user, streak, and preferences."""
    unique_email = f"test_success_{uuid.uuid4().hex[:8]}@codeorbit.local"
    payload = {
        "email": unique_email,
        "password": "Password123!",
        "confirm_password": "Password123!",
        "full_name": "Test Student",
        "college": "MIT College of Engineering",
        "degree": "B.Tech",
        "branch": "CSE",
        "graduation_year": 2026
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    user = data["user"]
    assert user["email"] == unique_email
    assert user["full_name"] == "Test Student"
    assert user["streak"]["current_streak"] == 0
    assert user["preferences"]["programming_level"] == "Intermediate"
    assert user["is_admin"] is False

def test_duplicate_email_registration():
    """Verify registering with an existing email returns HTTP 400 with a clear message."""
    unique_email = f"test_dup_{uuid.uuid4().hex[:8]}@codeorbit.local"
    payload = {
        "email": unique_email,
        "password": "Password123!",
        "confirm_password": "Password123!",
        "full_name": "Original User"
    }
    res1 = client.post("/api/auth/register", json=payload)
    assert res1.status_code == 200

    # Attempt second registration with same email
    res2 = client.post("/api/auth/register", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"].lower()

def test_password_mismatch():
    """Verify mismatched password and confirm_password returns HTTP 400."""
    payload = {
        "email": "test_mismatch@codeorbit.local",
        "password": "Password123!",
        "confirm_password": "DifferentPassword123!",
        "full_name": "Mismatch User"
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 400
    assert "passwords do not match" in res.json()["detail"].lower()

def test_invalid_email_format():
    """Verify malformed email addresses are rejected with HTTP 422."""
    payload = {
        "email": "not-an-email",
        "password": "Password123!",
        "confirm_password": "Password123!",
        "full_name": "Invalid Email User"
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 422

def test_short_password():
    """Verify password shorter than 6 characters is rejected with HTTP 422."""
    payload = {
        "email": "test_short@codeorbit.local",
        "password": "123",
        "confirm_password": "123",
        "full_name": "Short Pass User"
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 422

def test_long_password_bcrypt_limit():
    """Verify passwords exceeding 72 characters are safely handled or rejected."""
    long_pass = "A" * 75
    payload = {
        "email": "test_long@codeorbit.local",
        "password": long_pass,
        "confirm_password": long_pass,
        "full_name": "Long Password User"
    }
    res = client.post("/api/auth/register", json=payload)
    # Schema limits to max_length 72, returning 422
    assert res.status_code == 422

def test_database_failure_handling_and_rollback():
    """Verify that when a database operational error occurs, it is caught, rolled back, and returns 503."""
    payload = {
        "email": "test_db_fail@codeorbit.local",
        "password": "Password123!",
        "confirm_password": "Password123!",
        "full_name": "DB Fail User"
    }
    with patch("sqlalchemy.orm.Session.commit", side_effect=OperationalError("mock failure", None, None)):
        res = client.post("/api/auth/register", json=payload)
        assert res.status_code == 503
        data = res.json()
        assert "temporarily unavailable" in data["detail"].lower()
        # Ensure credentials/database connection string is NOT in response
        assert "password" not in data["detail"].lower()
        assert "postgresql" not in data["detail"].lower()
