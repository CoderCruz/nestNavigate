from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base


class AppUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True, nullable = False)
    name = Column(String, nullable = False)
    hashed_password = Column(String, nullable = False)
    coins_earned = Column(Integer, default = 0)
    created_at = Column(DateTime(timezone = True), server_default = func.now())


class LearningModule(Base):
    __tablename__ = "modules"

    id = Column(String, primary_key = True, index = True)
    title = Column(String, nullable = False)
    lessons = Column(String, nullable = False)
    total_coins = Column(Integer, default = 0)
    difficulty = Column(String)
