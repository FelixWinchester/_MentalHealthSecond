from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()

# Модели Pydantic для валидации данных

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Замените orm_mode на from_attributes

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class MoodEntryCreate(BaseModel):
    mood: str
    details: Optional[str] = None

class MoodEntryOut(MoodEntryCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Модели SQLAlchemy для базы данных

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    moods = relationship("MoodEntry", back_populates="user", cascade="all, delete-orphan")

class MoodEntry(Base):
    __tablename__ = "mood_entries"
    id = Column(Integer, primary_key=True, index=True) #Id записи
    user_id = Column(Integer, ForeignKey("users.id")) #у какого пользователя
    mood = Column(String, nullable=False)#какое настроение
    details = Column(String, nullable=True)#подробности текстовые типа заметок
    timestamp = Column(DateTime, default=datetime.utcnow)#время
    user = relationship("UserDB", back_populates="moods")#связь с табличкой UserDB