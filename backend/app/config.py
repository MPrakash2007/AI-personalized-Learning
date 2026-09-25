import os
import shutil
from typing import List, Union
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CodeOrbit"
    API_V1_STR: str = "/api"
    
    # Base directories
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # Security & Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "codeorbit_super_secret_jwt_key_2026_engineering_students")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # AI Provider configuration (OpenAI First)
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai")  # "openai", "rule-based", "ollama", "mock"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # CORS
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    def get_database_url(self) -> str:
        raw_url = (self.DATABASE_URL or os.getenv("DATABASE_URL", "")).strip()
        
        # If PostgreSQL URL provided
        if raw_url:
            # Handle Postgres dialect compatibility for SQLAlchemy (Neon, Supabase, Vercel Postgres provide postgres://)
            if raw_url.startswith("postgres://"):
                raw_url = raw_url.replace("postgres://", "postgresql://", 1)
            return raw_url

        # In Vercel production: NEVER silently fall back to /tmp SQLite.
        # Ephemeral filesystems drop all data across cold starts/instances.
        if os.getenv("VERCEL"):
            import sys
            sys.stderr.write("[CONFIG ERROR] DATABASE_URL is missing in Vercel environment variables. PostgreSQL is required for production.\n")
            sys.stderr.flush()
            return ""

        # Local development fallback to local SQLite
        local_db = os.path.join(self.BASE_DIR, "codeorbit.db")
        return f"sqlite:///{local_db}"

    def get_jwt_secret(self) -> str:
        secret = (self.JWT_SECRET or os.getenv("JWT_SECRET") or "").strip()
        if not secret:
            return "codeorbit_super_secret_jwt_key_2026_engineering_students"
        return secret

    def get_cors_origins(self) -> List[str]:
        origins = [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
        ]
        env_origins = os.getenv("CORS_ORIGINS", "")
        if env_origins:
            for item in env_origins.split(","):
                clean = item.strip()
                if clean and clean not in origins:
                    origins.append(clean)
        elif isinstance(self.CORS_ORIGINS, list):
            for item in self.CORS_ORIGINS:
                if item not in origins:
                    origins.append(item)
        elif isinstance(self.CORS_ORIGINS, str):
            for item in self.CORS_ORIGINS.split(","):
                clean = item.strip()
                if clean and clean not in origins:
                    origins.append(clean)
        return origins

    model_config = ConfigDict(case_sensitive=True, extra="ignore")

settings = Settings()
