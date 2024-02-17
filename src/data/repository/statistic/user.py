from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.statistic.user import MissionUserCounterDTO, TaskUserCounterDTO
from src.core.interfaces.repository.statistic.user import IRepositoryUserStatistic


class UserStatisticRepository(IRepositoryUserStatistic):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def task_counter(self, *, user_id: str) -> TaskUserCounterDTO:
        return await super().task_counter(user_id=user_id)

    async def mission_counter(self, *, user_id: str) -> MissionUserCounterDTO:
        return await super().mission_counter(user_id=user_id)
