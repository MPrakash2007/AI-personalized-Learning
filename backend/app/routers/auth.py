import logging
import sys
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool
from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError, ProgrammingError
from datetime import datetime, timezone
from app.config import settings
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
    
    # 0. Current user, database, schema
    try:
        user_info = db.execute(text("SELECT current_user, session_user, current_database(), current_schema();")).fetchone()
        results["postgres_context"] = {
            "current_user": user_info[0] if user_info else None,
            "session_user": user_info[1] if user_info else None,
            "database": user_info[2] if user_info else None,
            "schema": user_info[3] if user_info else None,
        }
    except Exception as e:
        results["postgres_context_error"] = sanitize_db_log(str(e))
        db.rollback()

    # 0b. What tables CAN authenticator/authenticated/PUBLIC access?
    try:
        grants = db.execute(text("SELECT grantee, table_schema, table_name, privilege_type FROM information_schema.role_table_grants WHERE grantee IN ('authenticator', 'authenticated', 'anonymous', 'PUBLIC');")).fetchall()
        results["grants_for_current_role"] = [{"grantee": r[0], "schema": r[1], "table": r[2], "privilege": r[3]} for r in grants]
    except Exception as e:
        db.rollback()
        results["grants_error"] = sanitize_db_log(str(e))

    # 0c. Role memberships
    try:
        members = db.execute(text("SELECT m.roleid::regrole::text, m.member::regrole::text FROM pg_auth_members m;")).fetchall()
        results["role_memberships"] = [{"role": r[0], "member": r[1]} for r in members]
    except Exception as e:
        db.rollback()
        results["role_memberships_error"] = sanitize_db_log(str(e))

    # 1. Existing tables from pg_catalog (bypasses information_schema permissions filter)
    try:
        pg_rows = db.execute(text("SELECT schemaname, tablename, tableowner FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema');")).fetchall()
        results["pg_tables"] = [{"schema": r[0], "table": r[1], "owner": r[2]} for r in pg_rows]
    except Exception as e:
        results["pg_tables_error"] = sanitize_db_log(str(e))
        db.rollback()

    # 2. Existing tables from information_schema
    try:
        table_rows = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")).fetchall()
        results["existing_tables"] = sorted([r[0] for r in table_rows])
    except Exception as e:
        results["tables_error"] = sanitize_db_log(str(e))
        db.rollback()

    # 3. Grants on users table
    try:
        grant_rows = db.execute(text("SELECT grantee, table_schema, table_name, privilege_type FROM information_schema.role_table_grants WHERE table_name='users';")).fetchall()
        results["users_grants"] = [{"grantee": r[0], "schema": r[1], "table": r[2], "privilege": r[3]} for r in grant_rows]
    except Exception as e:
        results["users_grants_error"] = sanitize_db_log(str(e))
        db.rollback()


    # 5. Existing columns of users from pg_catalog (bypasses information_schema permissions)
    try:
        col_rows = db.execute(text(
            "SELECT a.attname, format_type(a.atttypid, a.atttypmod) "
            "FROM pg_catalog.pg_attribute a "
            "JOIN pg_catalog.pg_class c ON a.attrelid = c.oid "
            "JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid "
            "WHERE n.nspname = 'public' AND c.relname = 'users' AND a.attnum > 0 AND NOT a.attisdropped "
            "ORDER BY a.attnum;"
        )).fetchall()
        results["users_columns_pg_catalog"] = {r[0]: r[1] for r in col_rows}
    except Exception as e:
        results["users_columns_pg_catalog_error"] = sanitize_db_log(str(e))
        db.rollback()

    # 5b. pg_roles inspection
    try:
        role_rows = db.execute(text("SELECT rolname, rolsuper, rolinherit, rolcreaterole, rolcreatedb, rolcanlogin FROM pg_roles;")).fetchall()
        results["pg_roles"] = [{"name": r[0], "super": r[1], "inherit": r[2], "create_role": r[3], "create_db": r[4], "can_login": r[5]} for r in role_rows]
    except Exception as e:
        results["pg_roles_error"] = sanitize_db_log(str(e))
        db.rollback()

    # 5c. Permissions on public schema and users table
    try:
        perm_test = db.execute(text("""
            SELECT
                has_schema_privilege('public', 'USAGE') as public_usage,
                has_schema_privilege('public', 'CREATE') as public_create,
                has_table_privilege('public.users', 'SELECT') as users_select,
                has_table_privilege('public.users', 'INSERT') as users_insert,
                has_table_privilege('public.users', 'UPDATE') as users_update
        """)).fetchone()
        results["authenticator_privileges"] = {
            "public_usage": perm_test[0] if perm_test else None,
            "public_create": perm_test[1] if perm_test else None,
            "users_select": perm_test[2] if perm_test else None,
            "users_insert": perm_test[3] if perm_test else None,
            "users_update": perm_test[4] if perm_test else None,
        }
    # 5d. Any procedures/functions in public or neon_auth?
    try:
        proc_rows = db.execute(text(
            "SELECT proname, pronamespace::regnamespace::text, prosecdef "
            "FROM pg_proc "
            "WHERE pronamespace::regnamespace::text IN ('public', 'neon_auth');"
        )).fetchall()
        results["custom_functions"] = [{"name": r[0], "schema": r[1], "security_definer": r[2]} for r in proc_rows]
    except Exception as e:
        results["custom_functions_error"] = sanitize_db_log(str(e))
        db.rollback()

    # 6. Test db.query(User).first()
    try:
        u = db.query(User).first()
        results["user_query"] = "success"
        results["user_found"] = bool(u)
    except Exception as e:
        db.rollback()
        orig = getattr(e, "orig", e)
        results["user_query_error"] = sanitize_db_log(f"{type(e).__name__}: {orig}")

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
