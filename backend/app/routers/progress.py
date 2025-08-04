from fastapi import APIRouter, Depends, HTTPException, Path, Body
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

    module = db.query(models.LearningModule).filter(models.LearningModule.id == data.module_id).first()
    if not module:
        raise HTTPException(status_code = 404, detail = "Module not found")

    if progress:
        completed_lessons = progress.lessons_completed.split(",") if progress.lessons_completed else []
        if data.lesson_name not in completed_lessons:
            completed_lessons.append(data.lesson_name)
            progress.lessons_completed = ",".join(completed_lessons)
            progress.last_accessed = datetime.utcnow()
            current_user.coins_earned += module.total_coins // len(module.lessons.split(","))
    else:
        progress = models.UserProgress(
            user_id=current_user.id,
            module_id=data.module_id,
            lessons_completed=data.lesson_name,
            last_accessed=datetime.utcnow()
        )
        db.add(progress)
        current_user.coins_earned += module.total_coins // len(module.lessons.split(","))

    db.commit()

    user_data = {
        "id": current_user.id,
        "name": current_user.name,
        "coins_earned": current_user.coins_earned
    }
    user_progress = db.query(models.UserProgress).filter_by(user_id=current_user.id).all()

    result_progress = []
    for p in user_progress:
        mod = db.query(models.LearningModule).filter(models.LearningModule.id == p.module_id).first()
        total_lessons = len(mod.lessons.split(",")) if mod else 0
        completed = len(p.lessons_completed.split(",")) if p.lessons_completed else 0
        completion_percentage = round((completed / total_lessons) * 100, 2) if total_lessons else 0

        result_progress.append({
            "module_id": p.module_id,
            "lessons_completed": p.lessons_completed.split(",") if p.lessons_completed else [],
            "completion_percentage": completion_percentage,
            "last_accessed": p.last_accessed
        })

    return {"user": user_data, "progress": result_progress}

@router.post("/coins/award")
def award_coins(
    user_id: int = Body(...),
    coins: int = Body(...),
    db: Session = Depends(database.get_db),
    current_user: models.AppUser = Depends(auth.get_current_user)
):
    user = db.query(models.AppUser).filter(models.AppUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    user.coins_earned += coins
    db.commit()
    db.refresh(user)
    return {"message": f"Awarded {coins} coins to {user.name}", "new_total": user.coins_earned}
