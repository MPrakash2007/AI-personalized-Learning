from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    email: str = Field(..., min_length=5)
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserPreferencesResponse(BaseModel):
    programming_level: str
    preferred_subjects: str
    daily_target_minutes: int
    career_goal: str
    theme: str
    sound_effects: bool
    daily_reminder: bool

    class Config:
        from_attributes = True

class StreakResponse(BaseModel):
    current_streak: int
    longest_streak: int
    freeze_count: int
    weekly_history: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    avatar_url: Optional[str] = None
    is_admin: bool
    level: int
    xp: int
    gems: int
    onboarding_completed: bool
    created_at: datetime
    streak: Optional[StreakResponse] = None
    preferences: Optional[UserPreferencesResponse] = None

    class Config:
        from_attributes = True

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
