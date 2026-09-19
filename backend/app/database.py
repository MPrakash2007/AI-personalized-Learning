import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.config import settings

logger = logging.getLogger("uvicorn.error")

db_url = settings.get_database_url()

engine_kwargs = {"echo": False, "future": True}

if db_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # Serverless-resilient PostgreSQL connection strategy
    # On Vercel / serverless: use NullPool to prevent connection exhaustion and stale socket errors
    if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        engine_kwargs["poolclass"] = NullPool
    else:
        engine_kwargs["pool_pre_ping"] = True
        engine_kwargs["pool_recycle"] = 300
        engine_kwargs["pool_size"] = 5
        engine_kwargs["max_overflow"] = 10

engine = create_engine(db_url, **engine_kwargs)

if db_url.startswith("sqlite"):
    from sqlalchemy import event
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

_schema_initialized = False

def init_db(force: bool = False) -> bool:
    """
    Safely and idempotently initializes database tables.
    Never crashes module import or startup if the database is temporarily unreachable.
    """
    global _schema_initialized
    if _schema_initialized and not force:
        return True
    try:
        import app.models  # noqa: F401
        Base.metadata.create_all(bind=engine)
        _schema_initialized = True
        logger.info("Database schema successfully synchronized.")
        return True
    except Exception as e:
        logger.warning(f"Database schema synchronization notice: {e}")
        return False

def check_db_connection() -> dict:
    """
    Safely probes database connectivity without leaking passwords or connection strings.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "connected", "dialect": engine.dialect.name}
    except Exception as e:
        logger.error(f"Database connectivity check failed: {type(e).__name__}")
        return {"status": "disconnected", "dialect": engine.dialect.name}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
