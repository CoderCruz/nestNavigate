from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, modules, progress
from app import models, database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#TODO: add vercel front end deployment when done, for CORS
origins = [
    "http://localhost:5173",
    "https://my-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind = engine)

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


app.include_router(users.router)
app.include_router(modules.router)
app.include_router(progress.router)

@app.get("/")
def health_check():
    return {"status": "Backend is running on PORT:8000"}
