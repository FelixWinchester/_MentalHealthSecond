from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from models import UserDB, Achievement, UserAchievementDB, UserAchievementOut
from auth import get_current_user
from database import get_db
from achievements import AchievementService


router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("/", response_model=list[Achievement])
async def get_all_achievements(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Achievement))
    return result.scalars().all()

@router.get("/user", response_model=list[UserAchievementOut])
async def get_user_achievements(
    current_user: UserDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserAchievementDB)
        .where(UserAchievementDB.user_id == current_user.id)
        .options(joinedload(UserAchievementDB.achievement))
    )
    return result.scalars().all()
