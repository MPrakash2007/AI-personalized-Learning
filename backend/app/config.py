import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "CodeOrbit"
    API_V1_STR: str = "/api"
    
    # Database
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'codeorbit.db')}")
    
    # Security & Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "codeorbit_super_secret_jwt_key_2026_engineering_students")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # AI Provider configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "rule-based")  # "ollama", "mock", "rule-based"
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    class Config:
        case_sensitive = True

settings = Settings()
