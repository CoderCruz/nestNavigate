from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import get_current_user
from app.schemas import AppUserOut



router = APIRouter(prefix="/api/users", tags=["Users"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model = schemas.AppUserOut)
def register_user(user: schemas.AppUserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.AppUser).filter(models.AppUser.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code = 400, detail = "Email in use, try again")

    hashed_pw = auth.hash_password(user.password)
    new_user = models.AppUser(
        email = user.email,
        name = user.name,
        hashed_password = hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model = schemas.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.AppUser).filter(models.AppUser.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code = 401, detail = "Incorrect email or password")

    access_token = auth.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model = AppUserOut)
def get_profile(current_user: models.AppUser = Depends(get_current_user)):
    return current_user
