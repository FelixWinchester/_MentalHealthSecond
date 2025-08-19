from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List
from datetime import datetime

from database import get_db
from models import NotificationDB, NotificationOut, UserDB
from auth import get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])

# Получить список уведомлений пользователя
@router.get("/", response_model=List[NotificationOut])
async def get_notifications(
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    result = await db.execute(
        select(NotificationDB).where(NotificationDB.user_id == current_user.id).order_by(NotificationDB.created_at.desc())
    )
    return result.scalars().all()

# Получить количество непрочитанных уведомлений
@router.get("/unread_count")
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    result = await db.execute(
        select(NotificationDB).where(
            NotificationDB.user_id == current_user.id,
            NotificationDB.is_read == False
        )
    )
    return {"unread_count": len(result.scalars().all())}

# Отметить уведомление как прочитанное
@router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    await db.execute(
        update(NotificationDB)
        .where(NotificationDB.id == notification_id, NotificationDB.user_id == current_user.id)
        .values(is_read=True)
    )
    await db.commit()
    return {"message": "Notification marked as read"}

async def create_notification(db: AsyncSession, user_id: int, message: str):
    notification = NotificationDB(
        user_id=user_id,
        message=message,
        created_at=datetime.utcnow(),
        is_read=False
    )
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return notification
