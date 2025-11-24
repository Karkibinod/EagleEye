# eagle_eye_api/services/auth_service.py
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta
from typing import Optional

from ..models.user import User
from ..config.settings import SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Password Utilities ---


def hash_password(password: str) -> str:
    # Ensures input is bytes for bcrypt
    password_bytes = str(password).encode('utf-8')
    return pwd_context.hash(password_bytes)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Ensures plain_password for verification is also bytes
    plain_password_bytes = str(plain_password).encode('utf-8')
    return pwd_context.verify(plain_password_bytes, hashed_password)

# --- Core Authentication Logic ---


def create_new_user(db: Session, user_data) -> User:
    # --- REVERTED FIX: Pass the string directly. The library is designed to handle this. ---
    hashed_pass = hash_password(user_data.password)

    db_user = User(
        user_id=user_data.user_id,
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pass,
        role=user_data.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
