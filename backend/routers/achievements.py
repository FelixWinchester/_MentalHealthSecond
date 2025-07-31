import random
from urllib import request
from fastapi import APIRouter, FastAPI, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, update, select  # Import select here
# from achievements import AchievementService
from database import AsyncSessionLocal, get_db, create_tables
from models import DAILY_QUESTIONS, Achievement, AchievementDB, DialogAnswer, DialogMessage, MoodType, MoodViewHistoryOut, UserAchievementDB, UserAchievementOut, UserCreate, User, Token, UserDB, MoodEntry, MoodEntryCreate, MoodEntryOut, MoodViewHistory
from database import get_db, create_tables
from models import MoodViewHistoryOut, UserCreate, User, Token, UserDB, MoodEntry, MoodEntryCreate, MoodEntryOut, MoodViewHistory, MoodChartPoint, MoodMap
from auth import get_password_hash, create_access_token, verify_password, get_current_user
from datetime import datetime, timedelta
from typing import Optional, List
import logging
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter(prefix="/achievemments", tags=["achievemments"])

# @app.get("/achievements", response_model=list[Achievement])
# async def get_all_achievements(db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Achievement))
#     return result.scalars().all()

# @app.get("/achievements", response_model=List[Achievement])
# async def get_achievements(db: AsyncSession = Depends(get_db)):
#     return db.query(AchievementDB).all()

# @app.get("/users/me/achievements", response_model=list[UserAchievementOut])
# async def get_user_achievements(
#     current_user: UserDB = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     result = await db.execute(
#         select(UserAchievementDB)
#         .where(UserAchievementDB.user_id == current_user.id)
#         .options(joinedload(UserAchievementDB.achievement))  # Eager load achievement # type: ignore
#         .order_by(UserAchievementDB.unlocked_at.desc())
#     )
#     return result.unique().scalars().all()

# @app.get("/users/me/streak")
# async def get_streak_info(
#     current_user: UserDB = Depends(get_current_user)
# ):
#     return {
#         "current_streak": current_user.current_streak,
#         "longest_streak": current_user.longest_streak,
#         "next_milestone": calculate_next_milestone(current_user.current_streak)
#     }

# def calculate_next_milestone(self, current: int):
#     milestones = [3, 7, 14, 30, 60, 90]
#     for m in milestones:
#         if current < m:
#             return {"days": m, "progress": current/m}
#     return None

# DEFAULT_ACHIEVEMENTS = [
#     Achievement(
#         name="Новичок",
#         description="Сделать первую запись",
#         icon="star",
#         condition="entries_1"
#     ),
#     Achievement(
#         name="Недельная серия",
#         description="7 дней подряд с записями",
#         icon="fire",
#         condition="streak_7"
#     ),
#     Achievement(
#         name="Месячник",
#         description="30 дней ведения дневника",
#         icon="calendar",
#         condition="entries_30"
#     )
# ]

# @app.on_event("startup")
# async def startup():
#     # Создаем таблицы
#     await create_tables()
    
#     # Добавляем дефолтные достижения
#     async with AsyncSessionLocal() as session:  # Используем фабрику сессий
#         try:
#             result = await session.execute(select(Achievement))
#             if not result.scalars().first():
#                 session.add_all(DEFAULT_ACHIEVEMENTS)
#                 await session.commit()
#                 print("Default achievements added")
#         except Exception as e:
#             print(f"Error adding achievements: {str(e)}")
#             await session.rollback()
#         finally:
#             await session.close()