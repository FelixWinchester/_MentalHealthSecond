import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from typing import List, Optional
from datetime import datetime, timezone

from database import get_db
from models import (
    UserDB, MoodEntry, MoodEntryCreate, MoodEntryOut, 
    MoodType, MoodViewHistory, MoodViewHistoryOut
)
from auth import get_current_user
from achievements import AchievementService  # Импорт из вашего файла

router = APIRouter(prefix="/mood", tags=["mood"])
@router.get("/", response_model=List[MoodEntryOut])
async def get_all_mood_entries(
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    
    result = await db.execute(
        select(MoodEntry)
        .where(MoodEntry.user_id == current_user.id)
        .order_by(MoodEntry.timestamp.desc())
    )
    entries = result.scalars().all()
    print(f"✅ [DEBUG] Найдено записей: {len(entries)}")
    return entries


@router.post("/", response_model=MoodEntryOut)
async def create_or_update_mood_event(
    mood_entry_data: MoodEntryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # --- ЛОГ 1: Что вообще пришло от фронтенда ---
    print(f"\n🔥🔥🔥 [DEBUG] START REQUEST")
    print(f"📥 Входящие данные (RAW): {mood_entry_data}")
    print(f"👤 Пользователь: {current_user.username} (ID: {current_user.id})")

    # 1. Проверка на пустой запрос
    if mood_entry_data.mood is None and mood_entry_data.details is None:
        print("❌ [DEBUG] Ошибка: Пустые данные")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Необходимо передать настроение или текст заметки"
        )

    # 2. Время
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    today_start = datetime.combine(now.date(), datetime.min.time())
    today_end = datetime.combine(now.date(), datetime.max.time())
    
    print(f"🕒 [DEBUG] Время сервера (UTC): {now}")

    try:
        # 3. Поиск записи
        print("🔍 [DEBUG] Ищем существующую запись...")
        result = await db.execute(
            select(MoodEntry).where(
                and_(
                    MoodEntry.user_id == current_user.id,
                    MoodEntry.timestamp >= today_start,
                    MoodEntry.timestamp <= today_end
                )
            )
        )
        existing_entry = result.scalars().first()
        print(f"📄 [DEBUG] Найдена запись? {'ДА (ID: ' + str(existing_entry.id) + ')' if existing_entry else 'НЕТ'}")

        # 4. Обработка Enum (САМОЕ ОПАСНОЕ МЕСТО)
        mood_enum = None
        if mood_entry_data.mood:
            raw_mood = mood_entry_data.mood
            print(f"🎭 [DEBUG] Пытаемся обработать настроение: '{raw_mood}'")
            try:
                # Попытка 1: Как есть
                mood_enum = MoodType(raw_mood)
                print(f"✅ [DEBUG] Успешно (прямое совпадение): {mood_enum}")
            except ValueError:
                print(f"⚠️ [DEBUG] Прямое совпадение не сработало. Пробуем .upper()...")
                try:
                    # Попытка 2: Верхний регистр
                    mood_enum = MoodType(raw_mood.upper())
                    print(f"✅ [DEBUG] Успешно (.upper()): {mood_enum}")
                except ValueError:
                    print(f"⚠️ [DEBUG] .upper() не сработал. Пробуем .lower()...")
                    try:
                        # Попытка 3: Нижний регистр
                        mood_enum = MoodType(raw_mood.lower())
                        print(f"✅ [DEBUG] Успешно (.lower()): {mood_enum}")
                    except ValueError:
                        print(f"❌ [DEBUG] FATAL: Значение '{raw_mood}' нет в Enum MoodType!")
                        print(f"📋 [DEBUG] Допустимые значения: {[e.value for e in MoodType]}")
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Неверное значение настроения: {raw_mood}"
                        )

        # 5. Логика сохранения
        entry_to_return = None
        if existing_entry:
            print("✏️ [DEBUG] Режим: ОБНОВЛЕНИЕ")
            if mood_enum:
                existing_entry.mood = mood_enum
            
            if mood_entry_data.details is not None:
                existing_entry.details = mood_entry_data.details
            
            existing_entry.timestamp = now
            entry_to_return = existing_entry
        else:
            print("✨ [DEBUG] Режим: СОЗДАНИЕ")
            new_entry = MoodEntry(
                user_id=current_user.id,
                mood=mood_enum,
                details=mood_entry_data.details,
                timestamp=now
            )
            db.add(new_entry)
            entry_to_return = new_entry

            # Стрики
            today_date = now.date()
            last_date = current_user.last_entry_date.date() if current_user.last_entry_date else None
            
            if last_date != today_date:
                # ... логика стриков (сократил для читаемости логов) ...
                print("🔥 [DEBUG] Обновляем стрики...")
                current_user.last_entry_date = now
                current_user.total_entries = (current_user.total_entries or 0) + 1

        print("💾 [DEBUG] Выполняем flush()...")
        await db.flush()
        
        print("🏆 [DEBUG] Проверка достижений...")
        achievement_service = AchievementService(db)
        # Обработка ошибок внутри сервиса достижений, чтобы не крашить всё
        try:
            await achievement_service.check_achievements(current_user)
        except Exception as ach_e:
            print(f"⚠️ [DEBUG] Ошибка в ачивках (игнорируем): {ach_e}")
            traceback.print_exc()

        print("✅ [DEBUG] COMMIT...")
        await db.commit()
        await db.refresh(entry_to_return)
        
        print("🚀 [DEBUG] УСПЕХ! Возвращаем ответ.")
        return entry_to_return

    except HTTPException as he:
        # Ловим наши же 400 ошибки и выводим их перед тем как отдать клиенту
        print(f"🛑 [DEBUG] CATCHED HTTP EXCEPTION: {he.detail}")
        raise he
    except Exception as e:
        print(f"☠️ [DEBUG] UNEXPECTED ERROR:")
        traceback.print_exc() # Выведет полный стек ошибки с номерами строк
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Server Error: {str(e)}"
        )

# --- ОСТАЛЬНЫЕ ЭНДПОИНТЫ ---

@router.get("/today", response_model=Optional[MoodEntryOut])
async def get_todays_entry(
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    today_start = datetime.combine(now.date(), datetime.min.time())
    result = await db.execute(
        select(MoodEntry).where(
            and_(
                MoodEntry.user_id == current_user.id,
                MoodEntry.timestamp >= today_start
            )
        )
    )
    return result.scalars().first()

@router.get("/analytics/moods")
async def get_mood_analytics(
    start_date: datetime,
    end_date: datetime,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    result = await db.execute(
        select(MoodEntry.mood, func.count(MoodEntry.id))
        .where(
            and_(
                MoodEntry.user_id == current_user.id,
                MoodEntry.timestamp.between(start_date, end_date),
                MoodEntry.mood.isnot(None)
            )
        )
        .group_by(MoodEntry.mood)
    )
    return {str(row[0].value if row[0] else "unknown"): row[1] for row in result.all()}

@router.get("/history/views", response_model=List[MoodViewHistoryOut])
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
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    return result.scalars().all()

@router.get("/{entry_id}", response_model=MoodEntryOut)
async def get_specific_entry(
    entry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    entry = await db.get(MoodEntry, entry_id)
    if not entry or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    view = MoodViewHistory(user_id=current_user.id, mood_entry_id=entry_id)
    db.add(view)
    await db.commit()
    return entry