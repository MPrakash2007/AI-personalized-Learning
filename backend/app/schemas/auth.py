import re
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=6, max_length=72)
    confirm_password: str = Field(..., min_length=6, max_length=72)
    full_name: str = Field(..., min_length=2, max_length=150)
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean = v.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", clean):
            raise ValueError("Invalid email address format.")
        return clean

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        clean = v.strip()
        if len(clean) < 2:
            raise ValueError("Full name must be at least 2 characters.")
        return clean

class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def clean_email(cls, v: str) -> str:
        return v.strip().lower()

class UserPreferencesResponse(BaseModel):
    programming_level: str = "Intermediate"
    preferred_subjects: str = "DBMS,DS,OS"
    daily_target_minutes: int = 30
    career_goal: str = "Placement preparation"
    theme: str = "dark"
    sound_effects: bool = True
    daily_reminder: bool = True

    model_config = ConfigDict(from_attributes=True)

class StreakResponse(BaseModel):
    current_streak: int = 0
    longest_streak: int = 0
    freeze_count: int = 1
    weekly_history: str = ""

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    avatar_url: Optional[str] = None
    is_admin: bool = False
    level: int = 1
    xp: int = 0
    gems: int = 100
    onboarding_completed: bool = False
    created_at: datetime
    streak: Optional[StreakResponse] = None
    preferences: Optional[UserPreferencesResponse] = None

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class OnboardingRequest(BaseModel):
    programming_level: str
    preferred_subjects: List[str]
    daily_target_minutes: int
    career_goal: str

class ForgotPasswordRequest(BaseModel):
    email: str

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    avatar_url: Optional[str] = None
    daily_target_minutes: Optional[int] = None
    theme: Optional[str] = None
    sound_effects: Optional[bool] = None
    daily_reminder: Optional[bool] = None

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)
