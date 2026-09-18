import os
import shutil
from typing import List, Union
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
    
    # AI Provider configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "rule-based")  # "ollama", "mock", "rule-based"
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # CORS
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    def get_database_url(self) -> str:
        raw_url = self.DATABASE_URL
        if not raw_url:
            # Fallback to local sqlite
            local_db = os.path.join(self.BASE_DIR, "codeorbit.db")
            raw_url = f"sqlite:///{local_db}"
        
        # Handle Postgres dialect compatibility for SQLAlchemy (Neon, Supabase, Vercel Postgres provide postgres://)
        if raw_url.startswith("postgres://"):
            raw_url = raw_url.replace("postgres://", "postgresql://", 1)
            
        # Handle Vercel serverless environment with SQLite fallback
        if raw_url.startswith("sqlite") and os.getenv("VERCEL"):
            tmp_db = "/tmp/codeorbit.db"
            src_db = os.path.join(self.BASE_DIR, "codeorbit.db")
            if not os.path.exists(tmp_db) and os.path.exists(src_db):
                try:
                    shutil.copyfile(src_db, tmp_db)
                except Exception:
                    pass
            if os.path.exists(tmp_db):
                raw_url = f"sqlite:///{tmp_db}"

        return raw_url

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

    class Config:
        case_sensitive = True

settings = Settings()
