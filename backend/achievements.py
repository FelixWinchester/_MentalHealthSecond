from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Achievement, UserAchievementDB, UserDB, AchievementDB

from datetime import datetime

from routers.notifications import create_notification

class AchievementService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_achievements(self, user: UserDB):
        achievements = await self.db.execute(select(AchievementDB))
        unlocked = []

        for achievement in achievements.scalars():
            if await self.check_condition(user, achievement.condition):
                if not await self.is_unlocked(user, achievement):
                    unlocked.append(achievement)
                    await self.unlock_achievement(user, achievement, commit=False)

        if unlocked:
            await self.db.commit()

        return [a.name for a in unlocked]


    async def check_condition(self, user: UserDB, condition: str):
        if condition == 'first_entry':
            return user.total_entries >= 1

        if condition.startswith('streak'):
            _, value = condition.split('_')
            return user.current_streak >= int(value)
    
        if condition.startswith('entries'):
            _, value = condition.split('_')
            return user.total_entries >= int(value)
    
        return False


    async def is_unlocked(self, user: UserDB, achievement: Achievement):
        result = await self.db.execute(
            select(UserAchievementDB).where(
                UserAchievementDB.user_id == user.id,
                UserAchievementDB.achievement_id == achievement.id
            )
        )
        return result.scalar() is not None

    async def unlock_achievement(self, user: UserDB, achievement: Achievement, commit: bool = True):
        user_achievement = UserAchievementDB(
            user_id=user.id,
            achievement_id=achievement.id,
            unlocked_at=datetime.utcnow()
            )
        self.db.add(user_achievement)
        if commit:
            await self.db.commit()
        
        await create_notification(
            self.db,
            user.id,
            f"Поздравляем! Вы получили достижение: {achievement.name}"
        )