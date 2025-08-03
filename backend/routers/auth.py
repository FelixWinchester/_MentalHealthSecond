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

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.info("Starting registration process")
    db_user = await db.execute(select(UserDB).where(UserDB.email == user.email))
    db_user = db_user.scalar()
    if db_user:
        logger.warning("Email already registered: %s", user.email)
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    logger.info("Password hashed successfully")
    db_user = UserDB(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    logger.info("User registered successfully: %s", user.username)
    return db_user

# Авторизация и получение токена
@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Ищем пользователя по username
        result = await db.execute(
            select(UserDB).where(UserDB.username == form_data.username)
        )
        user = result.scalar()

        if not user:
            logger.warning(f"Login attempt for non-existent user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Проверяем пароль
        if not verify_password(form_data.password, user.hashed_password):
            logger.warning(f"Invalid password for user: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Обновляем время последнего входа
        user.last_login = datetime.utcnow()
        await db.commit()
        await db.refresh(user)
        logger.info(f"User {user.username} successfully logged in")

        # Создаём токен
        access_token_expires = timedelta(minutes=60)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id  # Опционально, если нужно возвращать ID пользователя
        }

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error", 
        )
