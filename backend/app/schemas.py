from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List


class AppUserCreate(BaseModel):
    email: str
    name: str
    password: str

class AppUserOut(BaseModel):
    id: int
    email: str
    name: str
    coins_earned: int
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LearningModuleOut(BaseModel):
    id: str
    title: str
    lessons: str
    total_coins: int
    difficulty: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
