from enum import StrEnum
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Enum, Index, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()

class MoodType(StrEnum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    CALM = "calm"
    TIRED = "tired"
    EXCITED = "excited"
    ANXIOUS = "anxious"
    
#класс для работы графика
class MoodChartPoint(BaseModel):
    date: datetime
    mood: str

    class Config:
        from_attributes = True

class MoodMap:
    _mood_to_score = {
        "HAPPY": 5,
        "EXCITED": 5,
        "CALM": 4,
        "TIRED": 3,
        "SAD": 2,
        "ANXIOUS": 2,
        "ANGRY": 1,
    }
    
    @classmethod
    def get_score(cls, mood: str) -> int:
        """Возвращает числовой балл для настроения"""
        return cls._mood_to_score.get(mood.upper(), 3)  # 0 - значение по умолчанию
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
        from_attributes = True 

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

class MoodViewHistoryOut(BaseModel):
    id: int
    viewed_at: datetime
    mood_entry: MoodEntryOut

    class Config:
        from_attributes = True

# Модели SQLAlchemy для базы данных

class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(256))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    

    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_entry_date = Column(DateTime)
    total_entries = Column(Integer, default=0)
    
    # Отношения
    moods = relationship("MoodEntry", back_populates="user", cascade="all, delete-orphan")
    view_history = relationship("MoodViewHistory", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_user_email', "email"),
        Index('ix_user_created', "created_at"),
    )

class MoodEntry(Base):
    __tablename__ = "mood_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood = Column(Enum(MoodType), nullable=False)  # Исправлено здесь
    details = Column(String(500), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    


    # Отношения
    user = relationship("UserDB", back_populates="moods")
    views = relationship("MoodViewHistory", back_populates="mood_entry")

    __table_args__ = (
        Index('ix_mood_user', "user_id"),
        Index('ix_mood_timestamp', "timestamp"),
    )

class MoodViewHistory(Base):
    __tablename__ = "mood_view_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood_entry_id = Column(Integer, ForeignKey("mood_entries.id"))
    viewed_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    user = relationship("UserDB", back_populates="view_history")
    mood_entry = relationship("MoodEntry", back_populates="views")

    __table_args__ = (
        Index('ix_view_history', "user_id", "viewed_at"),
    )

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    icon = Column(String(100))
    condition = Column(String(50))  # Например: 'streak_7', 'entries_30'

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), primary_key=True)
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    achievement = relationship("Achievement")