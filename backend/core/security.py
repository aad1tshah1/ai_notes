from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.database import get_db
from services.auth_service import decode_access_token
from repositories.user_repository import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    user_id = decode_access_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user