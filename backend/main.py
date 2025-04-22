from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, update, select  # Import select here
from database import get_db, create_tables
from models import MoodViewHistoryOut, UserCreate, User, Token, UserDB, MoodEntry, MoodEntryCreate, MoodEntryOut, MoodViewHistory
from auth import get_password_hash, create_access_token, verify_password, get_current_user
from datetime import datetime, timedelta
from typing import Optional
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://10.7.0.12:8080"],  # Укажите домен вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание таблиц при запуске приложения
@app.on_event("startup")
async def startup():
    await create_tables()

# Регистрация пользователя
@app.post("/register", response_model=User)
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
@app.post("/token", response_model=Token)
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

# Защищённый эндпоинт
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: UserDB = Depends(get_current_user)):
    return current_user

# Обновление информации пользователя
@app.put("/users/me/update")
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

#эндпоинт для оценки настроения
@app.post("/mood", response_model=MoodEntryOut)
async def create_mood_entry(
    mood_entry: MoodEntryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    new_entry = MoodEntry(
        user_id=current_user.id,
        mood=mood_entry.mood,
        details=mood_entry.details
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry

@app.get("/me", response_model=User)
async def read_users_me(current_user: UserDB = Depends(get_current_user)):
    return current_user

@app.get("/mood/{entry_id}", response_model=MoodEntryOut)
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
@app.get("/analytics/moods")
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

@app.get("/history/views", response_model=list[MoodViewHistoryOut])
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


@app.get("/public")
async def public():
    return {"message": "Public endpoint works"}

@app.get("/private")
async def private(user: UserDB = Depends(get_current_user)):
    return {"message": f"Hello {user.username}", "email": user.email}