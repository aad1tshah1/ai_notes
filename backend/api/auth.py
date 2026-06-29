from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from services.auth_service import hash_password, verify_password, create_access_token
from core.database import get_db
from repositories.user_repository import create_user, get_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register_user(email: str, password: str, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = hash_password(password)

    user = create_user(db, email, password_hash)

    return {
        "user_id": str(user.user_id),
        "email": user.email,
        "message": "User registered successfully"
    }

@router.post("/login")
def log_in_user(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    password_verification = verify_password(form_data.password, user.password_hash)

    if not password_verification:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(str(user.user_id))

    return {
        "access_token": token,
        "token_type": "bearer",
    }
