from enum import Enum as PyEnum, StrEnum
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from sqlalchemy import (
    Column, Enum, Index, Integer, String, Text, 
    DateTime, ForeignKey, Boolean, Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()

# --- ENUMS & CONSTANTS ---

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

DAILY_QUESTIONS = [
    "Что сегодня вызвало у тебя улыбку?",
    "С каким чувством ты проснулся сегодня?",
    "Что было самым сложным за день?",
    "Как ты оцениваешь своё настроение от 1 до 5?",
    "Что ты сделал для себя сегодня?"
]

# --- КЛАССЫ ЛОГИКИ (Non-DB) ---

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
            return 3
        return cls._mood_to_score.get(mood_enum, 3)

# --- PYDANTIC SCHEMAS (Validation) ---

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    current_streak: int = 0
    longest_streak: int = 0
    total_entries: int = 0
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int

class TokenData(BaseModel):
    username: Optional[str] = None

class MoodEntryCreate(BaseModel):
    mood: Optional[str] = None
    details: Optional[str] = None

class MoodEntryOut(MoodEntryCreate):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True

class MoodChartPoint(BaseModel):
    date: datetime
    mood: str
    details: Optional[str]
    class Config:
        from_attributes = True

class MoodViewHistoryOut(BaseModel):
    id: int
    viewed_at: datetime
    mood_entry: MoodEntryOut
    class Config:
        from_attributes = True

class DialogAnswer(BaseModel):
    answer: str

# --- FORUM PYDANTIC SCHEMAS ---

class ThreadCreate(BaseModel):
    title: str
    content: str
    is_public: bool = True
    is_anonymous: bool = False
    allowed_user_ids: List[int] = []

class CommentCreate(BaseModel):
    content: str
    is_anonymous: bool = False

class VoteCreate(BaseModel):
    value: int  # 1 или -1

class ThreadOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    is_anonymous: bool
    author_name: str = "Пользователь"
    rating: int = 0
    comments_count: int = 0 
    user_vote: int = 0

    class Config:
        from_attributes = True

class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    author_name: Optional[str] = None
    rating: int = 0
    user_vote: Optional[int] = None
    class Config:
        from_attributes = True

# --- ACHIEVEMENT SCHEMAS ---

class AchievementBase(BaseModel):
    name: str
    description: str
    icon: str
    condition: str

class Achievement(AchievementBase):
    id: Optional[int] = None
    class Config:
        from_attributes = True

class AchievementOut(AchievementBase):
    id: int
    class Config:
        from_attributes = True

class UserAchievementOut(BaseModel):
    achievement: Achievement
    unlocked_at: datetime
    class Config:
        from_attributes = True

# --- SQLALCHEMY MODELS ---

# Таблица связи для приватных тредов (Many-to-Many)
thread_access = Table(
    "thread_access",
    Base.metadata,
    Column("thread_id", Integer, ForeignKey("threads.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
)

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
    threads = relationship("ThreadDB", back_populates="author")

    __table_args__ = (
        Index('ix_user_email', "email"),
        Index('ix_user_created', "created_at"),
    )

class MoodEntry(Base):
    __tablename__ = "mood_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood = Column(String(50), nullable=True)
    details = Column(String(500), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("UserDB", back_populates="moods")
    views = relationship("MoodViewHistory", back_populates="mood_entry")

    __table_args__ = (
        Index('ix_mood_user', "user_id"),
        Index('ix_mood_timestamp', "timestamp"),
    )

class ThreadDB(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    is_public = Column(Boolean, default=True)
    is_anonymous = Column(Boolean, default=False)
    
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("UserDB", back_populates="threads")
    
    comments = relationship("CommentDB", back_populates="thread", cascade="all, delete-orphan")
    allowed_users = relationship("UserDB", secondary=thread_access)
    votes = relationship("ThreadVote", cascade="all, delete-orphan")

class CommentDB(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey("threads.id", ondelete="CASCADE"))
    author_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_anonymous = Column(Boolean, default=False)

    thread = relationship("ThreadDB", back_populates="comments")
    author = relationship("UserDB")
    votes = relationship("CommentVote", cascade="all, delete-orphan")

class ThreadVote(Base):
    __tablename__ = "thread_votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    thread_id = Column(Integer, ForeignKey("threads.id", ondelete="CASCADE"), primary_key=True)
    value = Column(Integer) # 1 или -1

    # Добавляем уникальность, чтобы один юзер не мог иметь две записи для одного треда
    __table_args__ = (
        Index('ix_unique_user_vote', "user_id", "thread_id", unique=True),
    )

class CommentVote(Base):
    __tablename__ = "comment_votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), primary_key=True)
    value = Column(Integer)

class MoodViewHistory(Base):
    __tablename__ = "mood_view_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood_entry_id = Column(Integer, ForeignKey("mood_entries.id"))
    viewed_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("UserDB", back_populates="view_history")
    mood_entry = relationship("MoodEntry", back_populates="views")

    __table_args__ = (
        Index('ix_view_history', "user_id", "viewed_at"),
    )

class DialogMessage(Base):
    __tablename__ = "dialog_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    sender = Column(String(10), nullable=False)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserDB", back_populates="dialog_messages")

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
