from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, update, select  # Import select here
from backend.achievements import AchievementService
from database import AsyncSessionLocal, get_db, create_tables
from models import Achievement, MoodViewHistoryOut, UserAchievement, UserCreate, User, Token, UserDB, MoodEntry, MoodEntryCreate, MoodEntryOut, MoodViewHistory
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
    # Обновляем стрик
    today = datetime.utcnow().date()
    last_entry = current_user.last_entry_date.date() if current_user.last_entry_date else None
    
    if last_entry == today:
        raise HTTPException(status_code=400, detail="Entry already exists for today")
    
    if last_entry and (today - last_entry).days == 1:
        current_user.current_streak += 1
    else:
        current_user.current_streak = 1

    if current_user.current_streak > current_user.longest_streak:
        current_user.longest_streak = current_user.current_streak

    # Обновляем общее количество записей
    current_user.total_entries += 1
    current_user.last_entry_date = datetime.utcnow()

    # Создаем запись
    new_entry = MoodEntry(
        user_id=current_user.id,
        mood=mood_entry.mood,
        details=mood_entry.details
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)

    # Проверяем достижения
    service = AchievementService(db)
    unlocked = await service.check_achievements(current_user)

    return {
        "entry": new_entry,
        "unlocked_achievements": [a.name for a in unlocked]
    }

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


@app.get("/achievements", response_model=list[Achievement])
async def get_all_achievements(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Achievement))
    return result.scalars().all()

@app.get("/users/me/achievements", response_model=list[UserAchievement])
async def get_user_achievements(
    current_user: UserDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserAchievement)
        .where(UserAchievement.user_id == current_user.id)
        .order_by(UserAchievement.unlocked_at.desc())
    )
    return result.scalars().all()

@app.get("/users/me/streak")
async def get_streak_info(
    current_user: UserDB = Depends(get_current_user)
):
    return {
        "current_streak": current_user.current_streak,
        "longest_streak": current_user.longest_streak,
        "next_milestone": calculate_next_milestone(current_user.current_streak)
    }

def calculate_next_milestone(self, current: int):
    milestones = [3, 7, 14, 30, 60, 90]
    for m in milestones:
        if current < m:
            return {"days": m, "progress": current/m}
    return None

DEFAULT_ACHIEVEMENTS = [
    Achievement(
        name="Новичок",
        description="Сделать первую запись",
        icon="star",
        condition="entries_1"
    ),
    Achievement(
        name="Недельная серия",
        description="7 дней подряд с записями",
        icon="fire",
        condition="streak_7"
    ),
    Achievement(
        name="Месячник",
        description="30 дней ведения дневника",
        icon="calendar",
        condition="entries_30"
    )
]

@app.on_event("startup")
async def startup():
    # Создаем таблицы
    await create_tables()
    
    # Добавляем дефолтные достижения
    async with AsyncSessionLocal() as session:  # Используем фабрику сессий
        try:
            result = await session.execute(select(Achievement))
            if not result.scalars().first():
                session.add_all(DEFAULT_ACHIEVEMENTS)
                await session.commit()
                print("Default achievements added")
        except Exception as e:
            print(f"Error adding achievements: {str(e)}")
            await session.rollback()
        finally:
            await session.close()