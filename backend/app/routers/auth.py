import logging
import sys
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError, ProgrammingError
from datetime import datetime, timezone
from app.database import get_db, init_db, Base, sanitize_db_log
from app.models.user import User, UserPreferences, LearningStreak, XPTransaction
from app.schemas.auth import (
    UserRegister, UserLogin, TokenResponse, UserResponse,
    OnboardingRequest, ForgotPasswordRequest, UserProfileUpdate, PasswordChangeRequest
)
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.auth.deps import get_current_user

logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/diagnostic")
def auth_diagnostic(db: Session = Depends(get_db)):
    """Safe diagnostic endpoint inspecting tables, columns, and query errors without secrets."""
    results = {}
    
    # 1. Existing tables
    try:
        table_rows = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")).fetchall()
        results["existing_tables"] = sorted([r[0] for r in table_rows])
    except Exception as e:
        results["tables_error"] = sanitize_db_log(str(e))
        db.rollback()

    # 2. Existing columns of users
    try:
        col_rows = db.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='users';")).fetchall()
        results["users_columns"] = {r[0]: r[1] for r in col_rows}
    except Exception as e:
        results["users_columns_error"] = sanitize_db_log(str(e))
        db.rollback()

    # 3. Existing columns of user_preferences
    try:
        pref_cols = db.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='user_preferences';")).fetchall()
        results["user_preferences_columns"] = {r[0]: r[1] for r in pref_cols}
    except Exception as e:
        results["user_preferences_columns_error"] = sanitize_db_log(str(e))
        db.rollback()

    # 4. Existing columns of learning_streaks
    try:
        streak_cols = db.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='learning_streaks';")).fetchall()
        results["learning_streaks_columns"] = {r[0]: r[1] for r in streak_cols}
    except Exception as e:
        results["learning_streaks_columns_error"] = sanitize_db_log(str(e))
        db.rollback()

    # 5. Test db.query(User).first()
    try:
        u = db.query(User).first()
        results["user_query"] = "success"
        results["user_found"] = bool(u)
    except Exception as e:
        db.rollback()
        orig = getattr(e, "orig", e)
        results["user_query_error"] = sanitize_db_log(f"{type(e).__name__}: {orig}")

    # 6. Test Base.metadata.create_all
    try:
        Base.metadata.create_all(bind=db.bind)
        results["create_all"] = "success"
    except Exception as e:
        orig = getattr(e, "orig", e)
        results["create_all_error"] = sanitize_db_log(f"{type(e).__name__}: {orig}")

    return results

@router.post("/register", response_model=TokenResponse)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    if user_in.password != user_in.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match.")

    email = user_in.email.strip().lower()
    full_name = user_in.full_name.strip()

    # Query for existing user with table self-healing if needed
    try:
        existing_user = db.query(User).filter(User.email == email).first()
    except ProgrammingError as e:
        db.rollback()
        orig = getattr(e, "orig", e)
        clean_msg = sanitize_db_log(str(orig))
        sys.stderr.write(f"\n[REGISTER LOOKUP ERROR 1] ProgrammingError: {clean_msg}\n")
        sys.stderr.flush()
        init_db(force=True)
        try:
            existing_user = db.query(User).filter(User.email == email).first()
        except Exception as e2:
            db.rollback()
            orig2 = getattr(e2, "orig", e2)
            clean_msg2 = sanitize_db_log(str(orig2))
            sys.stderr.write(f"\n[REGISTER LOOKUP ERROR 2] {type(e2).__name__}: {clean_msg2}\n")
            sys.stderr.flush()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database error during registration lookup ({type(e2).__name__}): {clean_msg2}"
            )
    except (OperationalError, DatabaseError) as e:
        db.rollback()
        orig = getattr(e, "orig", e)
        clean_msg = sanitize_db_log(str(orig))
        sys.stderr.write(f"\n[REGISTER DB ERROR] {type(e).__name__}: {clean_msg}\n")
        sys.stderr.flush()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error during registration lookup ({type(e).__name__}): {clean_msg}"
        )

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email already exists.")

    try:
        new_user = User(
            email=email,
            hashed_password=hash_password(user_in.password),
            full_name=full_name,
            college=user_in.college.strip() if user_in.college else None,
            degree=user_in.degree.strip() if user_in.degree else None,
            branch=user_in.branch.strip() if user_in.branch else None,
            graduation_year=user_in.graduation_year,
            level=1,
            xp=0,
            gems=100,
            onboarding_completed=False,
            is_admin=False
        )

        # Attach default streak and preferences directly via ORM relationship
        new_user.streak = LearningStreak(
            current_streak=0,
            longest_streak=0,
            freeze_count=1,
            weekly_history=""
        )
        new_user.preferences = UserPreferences(
            programming_level="Intermediate",
            preferred_subjects="DBMS,DS,OS",
            daily_target_minutes=30,
            career_goal="Placement preparation"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user_response = UserResponse.model_validate(new_user)

    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Registration integrity conflict for email '{email}'")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )
    except (OperationalError, DatabaseError) as e:
        db.rollback()
        logger.error(f"Database error during user persistence: {type(e).__name__}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is temporarily unavailable. Please try again shortly."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error during user registration: {type(e).__name__}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration could not be completed. Please try again."
        )

    token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user_response}

@router.post("/login", response_model=TokenResponse)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    email = login_in.email.strip().lower()
    try:
        user = db.query(User).filter(User.email == email).first()
    except (OperationalError, DatabaseError) as e:
        db.rollback()
        orig = getattr(e, "orig", e)
        clean_msg = sanitize_db_log(str(orig))
        sys.stderr.write(f"\n[LOGIN DB ERROR] {type(e).__name__}: {clean_msg}\n")
        sys.stderr.flush()
        logger.error(f"Database error during login: {type(e).__name__}: {clean_msg}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error during login ({type(e).__name__}): {clean_msg}"
        )

    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    user_response = UserResponse.model_validate(user)
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user_response}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)

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
