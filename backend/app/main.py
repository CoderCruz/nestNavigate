from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, modules, progress
from app import models, database

app = FastAPI()

Base.metadata.create_all(bind = engine)

app.include_router(users.router)
app.include_router(modules.router)
app.include_router(progress.router)

with database.SessionLocal() as db:
    if db.query(models.LearningModule).count() == 0:
        sample_modules = [
            models.LearningModule(
                id="mod_1",
                title="test",
                lessons="test",
                total_coins=75,
                difficulty="Beginner"
            ),
            models.LearningModule(
                id="mod_2",
                title="test2",
                lessons="test2",
                total_coins=100,
                difficulty="Intermediate"
            )
        ]
        db.add_all(sample_modules)
        db.commit()


@app.get("/")
def health_check():
    return {"status": "Backend is running"}
