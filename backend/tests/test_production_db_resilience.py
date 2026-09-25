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

from app.config import settings, Settings
from app.database import (
    sanitize_db_log,
    get_engine,
    check_db_connection,
    engine,
    SessionLocal,
    Base
)
from app.main import app
from api.index import sanitize_log

client = TestClient(app)


def test_sanitize_log_masks_credentials():
    raw = "postgresql://alex:SuperSecret123@ep-sample-123456.us-east-2.aws.neon.tech/neondb?sslmode=require"
    cleaned = sanitize_log(raw)
    assert "SuperSecret123" not in cleaned
    assert ":***@" in cleaned
    assert "postgresql://alex:***@ep-sample-123456.us-east-2.aws.neon.tech/neondb?sslmode=require" == cleaned


def test_sanitize_log_masks_sensitive_keys():
    text = "JWT_SECRET=supersecret jwt=mytoken password=xyz API_KEY=abc1234"
    cleaned = sanitize_log(text)
    assert "supersecret" not in cleaned
    assert "xyz" not in cleaned
    assert "abc1234" not in cleaned
    assert "mytoken" not in cleaned


def test_postgres_url_conversion():
    s = Settings(DATABASE_URL="postgres://user:pass@host/db")
    converted = s.get_database_url()
    assert converted.startswith("postgresql+psycopg2://")
    assert not converted.startswith("postgres://")


def test_psycopg_v3_url_normalized_to_psycopg2():
    s = Settings(DATABASE_URL="postgresql+psycopg://user:pass@host/db")
    converted = s.get_database_url()
    assert converted.startswith("postgresql+psycopg2://")
    assert "postgresql+psycopg://" not in converted


def test_plain_postgresql_url_normalized_to_psycopg2():
    s = Settings(DATABASE_URL="postgresql://user:pass@host/db")
    converted = s.get_database_url()
    assert converted.startswith("postgresql+psycopg2://")


def test_postgresql_engine_driver_is_psycopg2():
    from sqlalchemy import create_engine
    eng = create_engine("postgresql+psycopg2://mockuser:mockpass@localhost:5432/mockdb")
    assert eng.dialect.name == "postgresql"
    assert eng.dialect.driver == "psycopg2"


def test_vercel_production_fails_without_database_url(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    s = Settings(DATABASE_URL="")
    assert s.get_database_url() == ""
    assert "sqlite" not in s.get_database_url()


def test_local_dev_uses_sqlite_fallback_when_no_db_url(monkeypatch):
    monkeypatch.delenv("VERCEL", raising=False)
    s = Settings(DATABASE_URL="")
    url = s.get_database_url()
    assert url.startswith("sqlite:///")


def test_health_check_endpoint_structure():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "service" in data
    assert data["service"] == "CodeOrbit API"
    assert "database" in data
    assert "dialect" in data
    assert data["status"] in ("healthy", "degraded")
    assert data["database"] in ("connected", "disconnected")


def test_health_check_reports_postgresql_when_connected(monkeypatch):
    from unittest.mock import patch, MagicMock
    mock_engine = MagicMock()
    mock_engine.dialect.name = "postgresql"
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    with patch("app.database.get_engine", return_value=mock_engine), \
         patch("app.database.init_db", return_value=True):
        diag = check_db_connection()
        assert diag["database"] == "connected"
        assert diag["dialect"] == "postgresql"

    with patch("app.main.check_db_connection", return_value={"database": "connected", "dialect": "postgresql"}):
        res = client.get("/api/health")
        assert res.status_code == 200
        body = res.json()
        assert body["status"] == "healthy"
        assert body["database"] == "connected"
        assert body["dialect"] == "postgresql"


def test_pg8000_url_sanitization():
    from urllib.parse import urlparse, parse_qs, urlencode
    url = "postgresql://usr:pwd@ep-xy-pooler.neon.tech/neondb?sslmode=require"
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)
    params.pop("sslmode", None)
    clean_query = urlencode(params, doseq=True)
    assert "sslmode" not in clean_query


def test_check_db_connection_diagnostic():
    diag = check_db_connection()
    assert "database" in diag
    assert "dialect" in diag
    assert diag["database"] in ("connected", "disconnected")

