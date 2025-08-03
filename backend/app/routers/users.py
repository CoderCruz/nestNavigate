from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth


router = APIRouter(prefix="/api/users", tags=["Users"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model = schemas.AppUserOut)
def register_user(user: schemas.AppUserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.AppUser).filter(models.AppUser.email === user.email).first()
    if existing_user:
        raise HTTPException(status_code = 400, details = "Email in use, try again")

    hashed_pw = auth.hash_password(user.password)
    new_user = models.AppUser(
        email = user.email,
        name = user.name,
        hashed_password = hased_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


