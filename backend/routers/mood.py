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


router = APIRouter(prefix="/mood", tags=["mood"])

#эндпоинт для оценки настроения
@router.post("/", response_model=MoodEntryOut)
async def create_mood_entry(
    mood_entry: MoodEntryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    today = datetime.utcnow().date()
    last_entry = current_user.last_entry_date.date() if current_user.last_entry_date else None

    if last_entry == today:
        raise HTTPException(status_code=400, detail="Entry already exists for today")

    if last_entry and (today - last_entry).days == 1:
        current_user.current_streak = (current_user.current_streak or 0) + 1
    else:
        current_user.current_streak = 1

    if (current_user.current_streak or 0) > (current_user.longest_streak or 0):
        current_user.longest_streak = current_user.current_streak

    current_user.total_entries = (current_user.total_entries or 0) + 1
    current_user.last_entry_date = datetime.utcnow()

    # Преобразуем строку настроения в MoodType enum
    try:
        mood_enum = MoodType(mood_entry.mood.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid mood value")

    new_entry = MoodEntry(
        user_id=current_user.id,
        mood=mood_enum,
        details=mood_entry.details
    )

    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)

    return new_entry


@router.get("/{entry_id}", response_model=MoodEntryOut)
async def get_mood_entry(
    entry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # Получение записи
    entry = await db.get(MoodEntry, entry_id)
    
    # Фиксация просмотра
    view = MoodViewHistory(
        user_id=current_user.id,
        mood_entry_id=entry_id
    )
    db.add(view)
    await db.commit()
    await db.refresh(entry)
    
    # Добавление счетчика просмотров
    entry.views_count = len(entry.views)
    return entry


# Получение статистики по настроениям
@router.get("/analytics/moods")
async def get_mood_analytics(
    start_date: datetime,
    end_date: datetime,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    result = await db.execute(
        select(
            MoodEntry.mood,
            func.count(MoodEntry.id)
        )
        .where(MoodEntry.user_id == current_user.id)
        .where(MoodEntry.timestamp.between(start_date, end_date))
        .group_by(MoodEntry.mood)
    )
    return dict(result.all())

@router.get("/history/views", response_model=list[MoodViewHistoryOut])
async def get_view_history(
    page: int = 1,
    per_page: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    result = await db.execute(
        select(MoodViewHistory)
        .where(MoodViewHistory.user_id == current_user.id)
        .order_by(MoodViewHistory.viewed_at.desc())
        .offset((page-1)*per_page)
        .limit(per_page)
    )
    return result.scalars().all()