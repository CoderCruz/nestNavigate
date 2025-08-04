from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import database, models
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-fallback-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)


def get_current_user(request: Request, db: Session = Depends(database.get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Missing authentication token",
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")
    except JWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")

    user = db.query(models.AppUser).filter(models.AppUser.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")

    return user

