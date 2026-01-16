from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserAchievementDB, UserDB, AchievementDB
from datetime import datetime, timezone

class AchievementService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_achievements(self, user: UserDB):
        # 1. Получаем ID уже имеющихся ачивок пользователя, чтобы не проверять их
        unlocked_result = await self.db.execute(
            select(UserAchievementDB.achievement_id)
            .where(UserAchievementDB.user_id == user.id)
        )
        already_had_ids = set(unlocked_result.scalars().all())

        # 2. Получаем только те ачивки, которых у пользователя еще НЕТ
        achievements_to_check = await self.db.execute(
            select(AchievementDB).where(AchievementDB.id.not_in(already_had_ids))
        )
        
        unlocked_names = []

        for achievement in achievements_to_check.scalars():
            if await self.check_condition(user, achievement.condition):
                # Просто добавляем в сессию, НЕ коммитим здесь
                await self.unlock_achievement(user, achievement)
                unlocked_names.append(achievement.name)

        # 3. Делаем flush, чтобы изменения ушли в БД, но транзакция осталась открытой
        if unlocked_names:
            await self.db.flush()

        return unlocked_names

    async def check_condition(self, user: UserDB, condition: str):
        # Логика условий (оставляем как была, она рабочая)
        if condition == 'first_entry':
            return (user.total_entries or 0) >= 1
        
        if condition.startswith('streak'):
            try:
                _, value = condition.split('_')
                return (user.current_streak or 0) >= int(value)
            except ValueError: return False
            
        if condition.startswith('entries'):
            try:
                _, value = condition.split('_')
                return (user.total_entries or 0) >= int(value)
            except ValueError: return False
            
        return False

    async def unlock_achievement(self, user: UserDB, achievement: AchievementDB):
        user_achievement = UserAchievementDB(
            user_id=user.id,
            achievement_id=achievement.id,
            unlocked_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )
        self.db.add(user_achievement)