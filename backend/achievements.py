from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserAchievementDB, UserDB, AchievementDB, MoodEntry
from datetime import datetime, timezone, timedelta

class AchievementService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_achievements(self, user: UserDB):
        unlocked_result = await self.db.execute(
            select(UserAchievementDB.achievement_id)
            .where(UserAchievementDB.user_id == user.id)
        )
        already_had_ids = set(unlocked_result.scalars().all())

        if already_had_ids:
            query = select(AchievementDB).where(AchievementDB.id.not_in(already_had_ids))
        else:
            query = select(AchievementDB)
        achievements_to_check = await self.db.execute(query)

        unlocked_names = []
        for achievement in achievements_to_check.scalars():
            if await self.check_condition(user, achievement.condition):
                await self.unlock_achievement(user, achievement)
                unlocked_names.append(achievement.name)

        if unlocked_names:
            await self.db.flush()

        return unlocked_names

    async def check_condition(self, user: UserDB, condition: str) -> bool:
        if condition == 'first_entry':
            result = await self.db.execute(
                select(func.count(MoodEntry.id)).where(MoodEntry.user_id == user.id)
            )
            return (result.scalar() or 0) >= 1

        if condition.startswith('streak_'):
            try:
                value = int(condition.split('_', 1)[1])
                streak = await self._get_current_streak(user.id)
                return streak >= value
            except (ValueError, IndexError):
                return False

        if condition.startswith('entries_'):
            try:
                value = int(condition.split('_', 1)[1])
                result = await self.db.execute(
                    select(func.count(MoodEntry.id)).where(MoodEntry.user_id == user.id)
                )
                return (result.scalar() or 0) >= value
            except (ValueError, IndexError):
                return False

        return False

    async def _get_current_streak(self, user_id: int) -> int:
        dates_result = await self.db.execute(
            select(func.date(MoodEntry.timestamp).label('entry_date'))
            .where(MoodEntry.user_id == user_id)
            .group_by(func.date(MoodEntry.timestamp))
            .order_by(func.date(MoodEntry.timestamp).desc())
        )
        dates = [row[0] for row in dates_result.fetchall()]

        today = datetime.now(timezone.utc).date()
        current_streak = 0
        if dates and dates[0] >= today - timedelta(days=1):
            expected = dates[0]
            for d in dates:
                if d == expected:
                    current_streak += 1
                    expected -= timedelta(days=1)
                else:
                    break
        return current_streak

    async def unlock_achievement(self, user: UserDB, achievement: AchievementDB):
        user_achievement = UserAchievementDB(
            user_id=user.id,
            achievement_id=achievement.id,
            unlocked_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )
        self.db.add(user_achievement)
