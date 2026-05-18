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


router = APIRouter(prefix="/users", tags=["users"])

# Защищённый эндпоинт
@router.get("/me", response_model=User)
async def read_users_me(current_user: UserDB = Depends(get_current_user)):
    return current_user

@router.get("/stats")
async def get_user_stats(
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    from datetime import timedelta, date as date_type

    total_result = await db.execute(
        select(func.count(MoodEntry.id)).where(MoodEntry.user_id == current_user.id)
    )
    total_entries = total_result.scalar() or 0

    ach_result = await db.execute(
        select(func.count(UserAchievementDB.achievement_id))
        .where(UserAchievementDB.user_id == current_user.id)
    )
    achievements_count = ach_result.scalar() or 0

    # Вычисляем текущую серию из реальных записей
    dates_result = await db.execute(
        select(func.date(MoodEntry.timestamp).label('entry_date'))
        .where(MoodEntry.user_id == current_user.id)
        .group_by(func.date(MoodEntry.timestamp))
        .order_by(func.date(MoodEntry.timestamp).desc())
    )
    dates = [row[0] for row in dates_result.fetchall()]

    today = datetime.utcnow().date()
    current_streak = 0
    if dates and dates[0] >= today - timedelta(days=1):
        expected = dates[0]
        for d in dates:
            if d == expected:
                current_streak += 1
                expected -= timedelta(days=1)
            else:
                break

    longest_streak = max(current_user.longest_streak or 0, current_streak)

    return {
        "total_entries": total_entries,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "achievements_count": achievements_count,
    }

# Обновление информации пользователя
@router.put("/me/update")
async def update_user_info(
    current_user: UserDB = Depends(get_current_user),
    username: Optional[str] = None,
    email: Optional[str] = None,
    avatar: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    update_data = {}
    if username:
        update_data["username"] = username
    if email:
        update_data["email"] = email
    if avatar:
        # Сохраняем файл на сервере и обновляем путь к аватару в базе данных
        avatar_path = f"static/avatars/{current_user.id}_{avatar.filename}"
        with open(avatar_path, "wb") as buffer:
            buffer.write(await avatar.read())
        update_data["avatar_path"] = avatar_path

    if update_data:
        await db.execute(update(UserDB).where(UserDB.id == current_user.id).values(**update_data))  
        await db.commit()

    return {"message": "User information updated successfully"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: UserDB = Depends(get_current_user)):
    return current_user


# Новый эндпоинт: получение чарта настроения
@router.get("/mood/chart", response_model=List[MoodChartPoint], tags=["Mood Chart"])
async def get_mood_chart(
    period: str = Query(
        "month",
        enum=["week", "two_weeks", "month", "three_months", "half_year", "year"]
    ),
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Эндпоинт для получения настроений пользователя за выбранный период.
    """
    today = datetime.utcnow()

    if period == "week":
        start_date = today - timedelta(weeks=1)
    elif period == "two_weeks":
        start_date = today - timedelta(weeks=2)
    elif period == "month":
        start_date = today - timedelta(days=30)
    elif period == "three_months":
        start_date = today - timedelta(days=90)
    elif period == "half_year":
        start_date = today - timedelta(days=180)
    elif period == "year":
        start_date = today - timedelta(days=365)
    else:
        start_date = today - timedelta(days=30)  # fallback

    result = await db.execute(
        select(MoodEntry)
        .where(MoodEntry.user_id == current_user.id)
        .where(MoodEntry.timestamp >= start_date)
        .order_by(MoodEntry.timestamp)
    )
    mood_entries = result.scalars().all()

    return [
        MoodChartPoint(
            date=entry.timestamp,
            mood=entry.mood,
            details=entry.details
        )
        for entry in mood_entries
    ]
    
# Новый эндпоинт для выдачи вердикта по настроению
@router.get("/mood/verdict", tags=["Mood Verdict"])
async def get_mood_verdict(
    period: str = Query(
        "month",
        enum=["week", "two_weeks", "month", "three_months", "half_year", "year"]
    ),
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Анализирует настроение пользователя за выбранный период и возвращает вердикт.
    """
    today = datetime.utcnow()

    if period == "week":
        start_date = today - timedelta(weeks=1)
    elif period == "two_weeks":
        start_date = today - timedelta(weeks=2)
    elif period == "month":
        start_date = today - timedelta(days=30)
    elif period == "three_months":
        start_date = today - timedelta(days=90)
    elif period == "half_year":
        start_date = today - timedelta(days=180)
    elif period == "year":
        start_date = today - timedelta(days=365)
    else:
        start_date = today - timedelta(days=30)  # fallback

    result = await db.execute(
        select(MoodEntry)
        .where(MoodEntry.user_id == current_user.id)
        .where(MoodEntry.timestamp >= start_date)
    )
    mood_entries = result.scalars().all()

    if not mood_entries:
        return {"verdict": "Недостаточно данных для анализа"}

    # Вычисляем среднее настроение через MoodMap
    mood_sum = sum(MoodMap.get_score(entry.mood) for entry in mood_entries)
    mood_avg = mood_sum / len(mood_entries)

    # Генерируем вердикт на основе среднего настроения
    if mood_avg >= 4.0:
        verdict = "Отличное настроение в последнее время!"
    elif 3.0 <= mood_avg < 4.0:
        verdict = "В целом всё нормально, но есть место для улучшений."
    elif 2.0 <= mood_avg < 3.0:
        verdict = "Настроение нестабильное, стоит обратить внимание на своё состояние."
    else:
        verdict = "Похоже, вы испытываете трудности. Рекомендуем обратиться за поддержкой."

    return {
        #"average_mood": mood_avg,
        "verdict": verdict
    }