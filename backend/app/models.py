from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
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


class UserProgress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    module_id = Column(String, ForeignKey("modules.id"), nullable=False)
    lessons_completed = Column(String, default="")  # comma-separated lessons
    last_accessed = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("AppUser")
    module = relationship("LearningModule")
