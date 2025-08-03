from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database, models, schemas, auth
from datetime import datetime

router = APIRouter(prefix = "/api/progress", tags = ["Progress"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/complete-lesson")
def complete_lesson(
    data: schemas.CompleteLessonInput,
    db: Session = Depends(get_db),
    current_user: models.AppUser = Depends(auth.get_current_user)
):
    progress = (
        db.query(models.UserProgress)
        .filter_by(user_id = current_user.id, module_id = data.module_id)
        .first()
    )

    if progress:
        completed_lessons = progress.lessons_completed.split(",") if progress.lessons_completed else []
        if data.lesson_name not in completed_lessons:
            completed_lessons.append(data.lesson_name)
            progress.lessons_completed = ",".join(completed_lessons)
            progress.last_accessed = datetime.utcnow()
    else:
        progress = models.UserProgress(
            user_id = current_user.id,
            module_id = data.module_id,
            lessons_completed = data.lesson_name,
            last_accessed = datetime.utcnow()
        )
        db.add(progress)

    db.commit()
    return {"message": "Lesson completed"}
