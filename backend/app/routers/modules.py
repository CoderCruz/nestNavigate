from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix = "/api/modules", tags = ["Modules"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model = list[schemas.LearningModuleOut])
def get_modules(db: Session = Depends(get_db)):
    return db.query(models.LearningModule).all()
