from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Achievement, UserAchievement, UserDB

class AchievementService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_achievements(self, user: UserDB):
        achievements = await self.db.execute(select(Achievement))
        unlocked = []

        for achievement in achievements.scalars():
            if await self.check_condition(user, achievement.condition):
                if not await self.is_unlocked(user, achievement):
                    unlocked.append(achievement)
                    await self.unlock_achievement(user, achievement)

        return unlocked

    async def check_condition(self, user: UserDB, condition: str):
        if condition.startswith('streak'):
            _, value = condition.split('_')
            return user.current_streak >= int(value)
        
        if condition.startswith('entries'):
            _, value = condition.split('_')
            return user.total_entries >= int(value)
        
        return False

    async def is_unlocked(self, user: UserDB, achievement: Achievement):
        result = await self.db.execute(
            select(UserAchievement).where(
                UserAchievement.user_id == user.id,
                UserAchievement.achievement_id == achievement.id
            )
        )
        return result.scalar() is not None

    async def unlock_achievement(self, user: UserDB, achievement: Achievement):
        user_achievement = UserAchievement(
            user_id=user.id,
            achievement_id=achievement.id
        )
        self.db.add(user_achievement)
        await self.db.commit()