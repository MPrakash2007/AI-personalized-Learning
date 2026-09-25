from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    try:
        user = db.query(User).filter(User.id == int(user_id)).first()
    except Exception as e:
        db.rollback()
        from app.database import sanitize_db_log
        import sys
        orig = getattr(e, "orig", e)
        clean_msg = sanitize_db_log(str(orig))
        sys.stderr.write(f"\n[GET_CURRENT_USER DB ERROR] {type(e).__name__}: {clean_msg}\n")
        sys.stderr.flush()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error during user authentication ({type(e).__name__}): {clean_msg}"
        )
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have administrative privileges."
        )
    return current_user
