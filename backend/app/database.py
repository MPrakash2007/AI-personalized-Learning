import os
import sys
import re
import ssl
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import NullPool
from fastapi import HTTPException, status

from app.config import settings

logger = logging.getLogger("uvicorn.error")

_engine = None
_session_factory = None
_schema_initialized = False

def sanitize_db_log(text_content: str) -> str:
    """Sanitize database connection strings and credentials from logs."""
    if not text_content:
        return ""
    # Redact username:password in database URLs
    sanitized = re.sub(
        r'(postgres(?:ql)?(?:\+[a-zA-Z0-9_-]+)?://)([^:@/\s]+):([^@/\s]+)@',
        r'\1\2:***@',
        text_content
    )
    sanitized = re.sub(
        r'(?i)(password|secret|key|token)\s*([=:])\s*([^\s,;&"\']+)',
        r'\1\2***',
        sanitized
    )
    return sanitized

def get_engine():
    """
    Lazily creates and returns the SQLAlchemy Engine.
    Ensures that module import NEVER fails due to missing or temporarily
    unreachable databases in serverless environments.
    """
    global _engine
    if _engine is not None:
        return _engine

    db_url = settings.get_database_url()
    if not db_url:
        if os.getenv("VERCEL"):
            sys.stderr.write("[DATABASE ERROR] DATABASE_URL is not set in Vercel environment variables.\n")
            sys.stderr.flush()
        return None

    engine_kwargs: Dict[str, Any] = {"echo": False, "future": True}

    if db_url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
        try:
            _engine = create_engine(db_url, **engine_kwargs)
            @event.listens_for(_engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
            return _engine
        except Exception as e:
            sys.stderr.write(f"[DATABASE ERROR] Failed to create SQLite engine: {type(e).__name__}\n")
            sys.stderr.flush()
            return None

    # Remote / PostgreSQL connection strategy
    is_serverless = bool(os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))
    if is_serverless:
        engine_kwargs["poolclass"] = NullPool
    else:
        engine_kwargs["pool_pre_ping"] = True
        engine_kwargs["pool_recycle"] = 300
        engine_kwargs["pool_size"] = 5
        engine_kwargs["max_overflow"] = 10

    # Test driver availability and configure dialect
    has_psycopg2 = False
    try:
        import psycopg2  # noqa: F401
        has_psycopg2 = True
    except ImportError:
        has_psycopg2 = False

    has_pg8000 = False
    try:
        import pg8000  # noqa: F401
        has_pg8000 = True
    except ImportError:
        has_pg8000 = False

    parsed = urlparse(db_url)
    is_remote = parsed.hostname not in ("localhost", "127.0.0.1", "::1", None)

    if has_psycopg2:
        # Use psycopg2 driver explicitly to prevent SQLAlchemy attempting to load psycopg (v3)
        if db_url.startswith("postgresql+psycopg://"):
            resolved_url = db_url.replace("postgresql+psycopg://", "postgresql+psycopg2://", 1)
        elif db_url.startswith("postgres://"):
            resolved_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif db_url.startswith("postgresql://"):
            resolved_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        else:
            resolved_url = db_url

        if is_remote:
            if "?" not in resolved_url:
                resolved_url += "?sslmode=require"
            elif "sslmode=" not in resolved_url:
                resolved_url += "&sslmode=require"
    elif has_pg8000:
        # Use pg8000 pure-Python driver
        # pg8000 does NOT accept 'sslmode' in query params (raises TypeError: connect() got unexpected keyword argument 'sslmode')
        query_params = parse_qs(parsed.query, keep_blank_values=True)
        query_params.pop("sslmode", None)
        clean_query = urlencode(query_params, doseq=True)
        resolved_url = urlunparse((
            "postgresql+pg8000",
            parsed.netloc,
            parsed.path,
            parsed.params,
            clean_query,
            parsed.fragment
        ))
        if is_remote:
            engine_kwargs["connect_args"] = {
                "ssl_context": ssl.create_default_context()
            }
    else:
        sys.stderr.write("[DATABASE ERROR] Neither psycopg2 nor pg8000 driver is available.\n")
        sys.stderr.flush()
        return None

    try:
        _engine = create_engine(resolved_url, **engine_kwargs)
        return _engine
    except Exception as e:
        clean_err = sanitize_db_log(f"{type(e).__name__}: {e}")
        sys.stderr.write(f"[DATABASE ERROR] Failed to construct engine: {clean_err}\n")
        sys.stderr.flush()
        return None

class SafeSessionFactory:
    """
    SessionLocal proxy that lazily resolves the engine on first query execution.
    Provides compatibility with sessionmaker usage in tests, routers, and scripts.
    """
    def __init__(self):
        self._custom_bind = None
        self._underlying = None

    def __call__(self, **kwargs) -> Session:
        eng = self._custom_bind or get_engine()
        if eng is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="CodeOrbit database service is not configured. Please ensure DATABASE_URL is set in Vercel environment variables."
            )
        if self._underlying is None or (self._custom_bind and self._underlying.kw.get("bind") != self._custom_bind):
            self._underlying = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=eng)
        return self._underlying(**kwargs)

    def configure(self, **kwargs):
        if "bind" in kwargs:
            self._custom_bind = kwargs["bind"]
        if self._underlying:
            self._underlying.configure(**kwargs)
        else:
            self._underlying = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, **kwargs)

    @property
    def bind(self):
        return self._custom_bind or get_engine()

class EngineProxy:
    """
    Proxy for the SQLAlchemy Engine to allow top-level module imports
    without triggering immediate connection or parsing failures.
    """
    def __getattr__(self, name: str):
        eng = get_engine()
        if eng is None:
            raise RuntimeError("Database engine is not initialized. Please configure DATABASE_URL.")
        return getattr(eng, name)

    def __bool__(self):
        return get_engine() is not None

    def __repr__(self):
        eng = get_engine()
        return repr(eng) if eng else "<EngineProxy: uninitialized>"

engine = EngineProxy()
SessionLocal = SafeSessionFactory()
Base = declarative_base()

def init_db(force: bool = False) -> bool:
    """
    Safely and idempotently initializes database tables using Base.metadata.create_all().
    Never crashes module import or startup if the database is temporarily unreachable.
    Does NOT execute heavy curriculum data seeding on cold start.
    """
    global _schema_initialized
    if _schema_initialized and not force:
        return True
    try:
        import app.models  # noqa: F401
        eng = get_engine()
        if eng is None:
            logger.warning("Database schema init skipped: engine is not configured.")
            return False
        Base.metadata.create_all(bind=eng)
        
        # Safe non-destructive schema upgrade for existing tables (Postgres & SQLite)
        try:
            with eng.connect() as conn:
                dialect = eng.dialect.name
                if "postgres" in dialect:
                    conn.execute(text("ALTER TABLE chat_sessions ADD COLUMN IF NOT EXISTS subject VARCHAR(100);"))
                    conn.execute(text("CREATE INDEX IF NOT EXISTS ix_chat_sessions_user_id ON chat_sessions(user_id);"))
                    conn.execute(text("CREATE INDEX IF NOT EXISTS ix_chat_sessions_updated_at ON chat_sessions(updated_at);"))
                    conn.execute(text("CREATE INDEX IF NOT EXISTS ix_chat_messages_session_id ON chat_messages(session_id);"))
                    conn.execute(text("CREATE INDEX IF NOT EXISTS ix_chat_messages_created_at ON chat_messages(created_at);"))
                    conn.commit()
                elif "sqlite" in dialect:
                    res = conn.execute(text("PRAGMA table_info(chat_sessions);")).fetchall()
                    cols = [r[1] for r in res]
                    if cols and "subject" not in cols:
                        conn.execute(text("ALTER TABLE chat_sessions ADD COLUMN subject VARCHAR(100);"))
                        conn.commit()
        except Exception as migration_err:
            clean_mig = sanitize_db_log(str(migration_err))
            logger.warning(f"Schema upgrade notice: {clean_mig}")

        _schema_initialized = True
        logger.info("Database schema successfully synchronized.")
        return True
    except Exception as e:
        clean_err = sanitize_db_log(f"{type(e).__name__}: {e}")
        logger.warning(f"Database schema synchronization notice: {clean_err}")
        return False

def check_db_connection() -> dict:
    """
    Safe diagnostic function that verifies database connectivity:
    1. DATABASE_URL existence
    2. Engine construction
    3. Driver availability
    4. Execution of 'SELECT 1'
    Never leaks credentials or sensitive connection strings.
    """
    db_url = settings.get_database_url()
    if not db_url:
        return {
            "database": "disconnected",
            "dialect": "none",
            "detail": "DATABASE_URL is missing in environment variables."
        }

    eng = get_engine()
    if eng is None:
        return {
            "database": "disconnected",
            "dialect": "unknown",
            "detail": "SQLAlchemy engine could not be constructed."
        }

    try:
        with eng.connect() as conn:
            conn.execute(text("SELECT 1"))
        init_db()
        dialect_name = eng.dialect.name
        return {
            "database": "connected",
            "dialect": "postgresql" if "postgres" in dialect_name else dialect_name
        }
    except Exception as e:
        clean_err = sanitize_db_log(f"{type(e).__name__}: {e}")
        sys.stderr.write(f"[DATABASE PROBE FAILED] {clean_err}\n")
        sys.stderr.flush()
        return {
            "database": "disconnected",
            "dialect": getattr(eng, "dialect", None) and eng.dialect.name or "unknown",
            "detail": f"Connection probe failed: {type(e).__name__}"
        }

def get_db():
    """FastAPI database session dependency."""
    global _schema_initialized
    if not _schema_initialized:
        init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

