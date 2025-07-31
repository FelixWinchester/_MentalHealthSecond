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
    SATISFIED = "satisfied"
    ANGRY = "angry"
    EXCITED = "excited"
    JOYFUL = "joyful"
    MISUNDERSTANDING = "misunderstanding"
    WORRIED = "worried"
    SAD = "sad"
    DEPRESSED = "depressed"
    
#класс для работы графика
class MoodChartPoint(BaseModel):
    date: datetime
    mood: str
    details: Optional[str]

    class Config:
        from_attributes = True

class MoodMap:
    _mood_to_score = {
        MoodType.HAPPY: 5,
        MoodType.EXCITED: 5,
        MoodType.SATISFIED: 4,
        MoodType.JOYFUL: 4,
        MoodType.MISUNDERSTANDING: 3,
        MoodType.WORRIED: 3,
        MoodType.SAD: 2,
        MoodType.DEPRESSED: 1,
        MoodType.ANGRY: 1,
    }
    
    @classmethod
    def get_score(cls, mood: str) -> int:
        """Возвращает числовой балл для настроения"""
        try:
            mood_enum = MoodType(mood.lower())
        except ValueError:
            return 3  # или любое значение по умолчанию

        return cls._mood_to_score.get(mood_enum, 3)
    
DAILY_QUESTIONS = [
    "Что сегодня вызвало у тебя улыбку?",
    "С каким чувством ты проснулся сегодня?",
    "Что было самым сложным за день?",
    "Как ты оцениваешь своё настроение от 1 до 5?",
    "Что ты сделал для себя сегодня?"
]

class DialogAnswer(BaseModel):
    answer: str


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
    user_id: int

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
    dialog_messages = relationship("DialogMessage", back_populates="user", cascade="all, delete-orphan")


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

class DialogMessage(Base):
    __tablename__ = "dialog_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    sender = Column(String(10), nullable=False)  # 'system' или 'user'
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Отношения
    user = relationship("UserDB", back_populates="dialog_messages")


class AchievementBase(BaseModel):
    name: str
    description: str
    icon: str
    condition: str

class Achievement(AchievementBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True

class AchievementCreate(AchievementBase):
    pass

class AchievementOut(AchievementBase):
    id: int

    class Config:
        from_attributes = True

class UserAchievementOut(BaseModel):
    achievement: Achievement
    unlocked_at: datetime

    class Config:
        from_attributes = True

# SQLAlchemy Models (renamed)
class AchievementDB(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    icon = Column(String(100))
    condition = Column(String(50))

class UserAchievementDB(Base):
    __tablename__ = "user_achievements"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), primary_key=True)
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    achievement = relationship("AchievementDB")