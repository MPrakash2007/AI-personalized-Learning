from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db
from app.models.user import User, UserPreferences, LearningStreak, XPTransaction
from app.schemas.auth import (
    UserRegister, UserLogin, TokenResponse, UserResponse,
    OnboardingRequest, ForgotPasswordRequest, UserProfileUpdate, PasswordChangeRequest
)
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.auth.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    if user_in.password != user_in.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="A user with this email already exists.")

    new_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        full_name=user_in.full_name,
        college=user_in.college,
        degree=user_in.degree,
        branch=user_in.branch,
        graduation_year=user_in.graduation_year,
        level=1,
        xp=0,
        gems=100,
        onboarding_completed=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Initialize default streak and preferences
    streak = LearningStreak(
        user_id=new_user.id,
        current_streak=0,
        longest_streak=0,
        freeze_count=1,
        weekly_history=""
    )
    prefs = UserPreferences(
        user_id=new_user.id,
        programming_level="Intermediate",
        preferred_subjects="DBMS,DS,OS",
        daily_target_minutes=30,
        career_goal="Placement preparation"
    )
    db.add(streak)
    db.add(prefs)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer", "user": new_user}

@router.post("/login", response_model=TokenResponse)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/onboarding", response_model=UserResponse)
def complete_onboarding(
    req: OnboardingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.onboarding_completed = True
    if current_user.preferences:
        current_user.preferences.programming_level = req.programming_level
        current_user.preferences.preferred_subjects = ",".join(req.preferred_subjects)
        current_user.preferences.daily_target_minutes = req.daily_target_minutes
        current_user.preferences.career_goal = req.career_goal
    else:
        prefs = UserPreferences(
            user_id=current_user.id,
            programming_level=req.programming_level,
            preferred_subjects=",".join(req.preferred_subjects),
            daily_target_minutes=req.daily_target_minutes,
            career_goal=req.career_goal
        )
        db.add(prefs)

    # Award first bonus onboarding XP (+50 XP)
    if current_user.xp == 0:
        current_user.xp += 50
        tx = XPTransaction(user_id=current_user.id, amount=50, reason="Completed Student Onboarding")
        db.add(tx)

    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    # Return friendly message even if email doesn't exist for security
    return {"message": f"If an account exists for {req.email}, reset instructions have been dispatched."}

@router.put("/profile", response_model=UserResponse)
def update_profile(
    update_in: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if update_in.full_name is not None:
        current_user.full_name = update_in.full_name
    if update_in.college is not None:
        current_user.college = update_in.college
    if update_in.degree is not None:
        current_user.degree = update_in.degree
    if update_in.branch is not None:
        current_user.branch = update_in.branch
    if update_in.graduation_year is not None:
        current_user.graduation_year = update_in.graduation_year
    if update_in.avatar_url is not None:
        current_user.avatar_url = update_in.avatar_url

    if current_user.preferences:
        if update_in.daily_target_minutes is not None:
            current_user.preferences.daily_target_minutes = update_in.daily_target_minutes
        if update_in.theme is not None:
            current_user.preferences.theme = update_in.theme
        if update_in.sound_effects is not None:
            current_user.preferences.sound_effects = update_in.sound_effects
        if update_in.daily_reminder is not None:
            current_user.preferences.daily_reminder = update_in.daily_reminder

    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/change-password")
def change_password(
    req: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(req.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect.")
    current_user.hashed_password = hash_password(req.new_password)
    db.commit()
    return {"message": "Password updated successfully."}
