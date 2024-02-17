from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.statistic.group import GroupMissionCounterDTO
from src.core.interfaces.repository.statistic.group import IRepositoryGroupStatistic


class GroupStatisticRepository(IRepositoryGroupStatistic):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def mission_counter(self, *, group_id: int) -> GroupMissionCounterDTO:
        return await super().mission_counter(group_id=group_id)
