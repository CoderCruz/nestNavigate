from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import get_current_user
from app.schemas import AppUserOut
from app.models import UserProgress, LearningModule

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

    access_token = auth.create_access_token(data = {"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model = AppUserOut)
def get_profile(current_user: models.AppUser = Depends(get_current_user)):
    return current_user


@router.get("/progress/{user_id}")
def get_user_progress(
    user_id: int = Path(..., gt = 0),
    db: Session = Depends(get_db),
    current_user: models.AppUser = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code = 403, detail = "Not authorized to view this progress.")

    progress_entries = db.query(models.UserProgress).filter(models.UserProgress.user_id == user_id).all()

    result = []
    for progress in progress_entries:
        module = db.query(models.LearningModule).filter(models.LearningModule.id == progress.module_id).first()
        total_lessons = len(module.lessons.split(",")) if module else 0 
        completed = len(progress.lessons_completed.split(",")) if progress.lessons_completed else 0
        completion_percentage = round((completed / total_lessons) * 100, 2) if total_lessons else 0
        result.append({
            "module_id": progress.module_id,
            "lessons_completed": progress.lessons_completed.split(",") if progress.lessons_completed else [],
            "completion_percentage": completion_percentage,
            "last_accessed": progress.last_accessed
        })

    return result
