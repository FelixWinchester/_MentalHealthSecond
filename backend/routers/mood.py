from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, update, select, and_  # Import select here
from database import AsyncSessionLocal, get_db, create_tables
from models import DAILY_QUESTIONS, MoodType, MoodViewHistoryOut, UserDB, MoodEntry, MoodEntryCreate, MoodEntryOut, MoodViewHistory
from database import get_db, create_tables
from models import MoodViewHistoryOut, UserDB, MoodEntry, MoodEntryCreate, MoodEntryOut, MoodViewHistory
from auth import get_current_user
from datetime import datetime,date
from achievements import AchievementService

from routers.notifications import create_notification

router = APIRouter(prefix="/mood", tags=["mood"])

#эндпоинт для оценки настроения
@router.post("/", response_model=MoodEntryOut)
async def create_or_update_mood_entry(
    mood_entry_data: MoodEntryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # 1. Проверяем, что передана эмоция
    if not mood_entry_data.mood:
        raise HTTPException(status_code=400, detail="Mood cannot be empty")
    
    # Преобразуем строку настроения в MoodType enum
    try:
        mood_enum = MoodType(mood_entry_data.mood.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid mood value")

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)

    # 2. Ищем существующую запись за сегодня
    result = await db.execute(
        select(MoodEntry)
        .where(
            and_(
                MoodEntry.user_id == current_user.id,
                MoodEntry.timestamp >= today_start,
                MoodEntry.timestamp <= today_end
            )
        )
    )
    existing_entry = result.scalars().first()

    # 3. Если запись существует - ОБНОВЛЯЕМ её
    if existing_entry:
        existing_entry.mood = mood_enum
        existing_entry.details = mood_entry_data.details
        # Обновляем время, чтобы было актуальным
        existing_entry.timestamp = datetime.utcnow() 
        db.add(existing_entry)
        await db.commit()
        await db.refresh(existing_entry)
        return existing_entry
    
    # 4. Если записи нет - СОЗДАЕМ новую и обновляем статистику пользователя
    else:
        # --- Логика для новой записи (подсчет серий и т.д.) ---
        today = date.today()
        last_entry_date = current_user.last_entry_date
        
        # Обновляем серию (streak)
        if last_entry_date and (today - last_entry_date).days == 1:
            current_user.current_streak = (current_user.current_streak or 0) + 1
        elif not (last_entry_date and last_entry_date == today):
             current_user.current_streak = 1
        
        if (current_user.current_streak or 0) > (current_user.longest_streak or 0):
            current_user.longest_streak = current_user.current_streak
            
        current_user.total_entries = (current_user.total_entries or 0) + 1
        current_user.last_entry_date = today # Используем date, а не datetime
        # --- Конец логики для новой записи ---
        
        await create_notification(
            db,
            current_user.id,
            "Вы успешно добавили запись о настроении!"
        )

        new_entry = MoodEntry(
            user_id=current_user.id,
            mood=mood_enum,
            details=mood_entry_data.details
        )
        db.add(new_entry)
        await db.flush() # Получаем ID для new_entry

        # Проверка достижений
        achievement_service = AchievementService(db)
        unlocked = await achievement_service.check_achievements(current_user)
        if unlocked:
            print("Разблокированы достижения:", ", ".join(unlocked))

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

@router.get("/today", response_model=MoodEntryOut)
async def get_todays_mood_entry(
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Возвращает запись о настроении пользователя за сегодняшний день, если она есть.
    """
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)

    result = await db.execute(
        select(MoodEntry)
        .where(
            and_(
                MoodEntry.user_id == current_user.id,
                MoodEntry.timestamp >= today_start,
                MoodEntry.timestamp <= today_end
            )
        )
    )
    todays_entry = result.scalars().first()
    
    if not todays_entry:
        raise HTTPException(status_code=404, detail="No mood entry found for today")
        
    return todays_entry

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