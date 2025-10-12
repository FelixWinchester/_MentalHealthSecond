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
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from config import settings



router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

@router.get("/google/login")
async def login_google(request: Request):
    # Генерируем URL для перенаправления на Google
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def auth_google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        # Получаем токен от Google
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        logger.error(f"OAuth error: {error}")
        return JSONResponse({"error": "Authentication failed"}, status_code=400)
    
    # Получаем информацию о пользователе
    userinfo = token.get('userinfo')
    if not userinfo:
        logger.error("No userinfo in token")
        return JSONResponse({"error": "Authentication failed"}, status_code=400)
    
    # Извлекаем данные пользователя
    email = userinfo.get('email')
    name = userinfo.get('name')
    google_id = userinfo.get('sub')
    
    if not email:
        logger.error("No email in userinfo")
        return JSONResponse({"error": "Email not provided by Google"}, status_code=400)
    
    # Проверяем, существует ли пользователь в нашей базе
    result = await db.execute(select(UserDB).where(UserDB.email == email))
    user = result.scalar()
    
    if not user:
        # Создаем нового пользователя
        username = email.split('@')[0]
        # Убедимся, что имя пользователя уникально
        counter = 1
        original_username = username
        while True:
            result = await db.execute(select(UserDB).where(UserDB.username == username))
            if not result.scalar():
                break
            username = f"{original_username}{counter}"
            counter += 1
        
        user = UserDB(
            username=username,
            email=email,
            google_id=google_id,
            hashed_password=None,  # У пользователей OAuth нет пароля
            is_oauth=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"New user created via Google OAuth: {username}")
    else:
        # Обновляем google_id если его нет
        if not user.google_id:
            user.google_id = google_id
            user.is_oauth = True
            await db.commit()
            await db.refresh(user)
    
    # Обновляем время последнего входа
    user.last_login = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    
    # Создаем JWT токен для нашего приложения
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    frontend_url = "http://localhost:3000"  # Замените на URL вашего фронтенда
    return RedirectResponse(
        url=f"{frontend_url}/auth/callback?token={access_token}&user_id={user.id}"
    )

@router.get("/google/logout")
async def logout_google():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response




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


