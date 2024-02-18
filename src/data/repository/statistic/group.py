from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.statistic.group import GroupMissionCounterDTO
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.interfaces.repository.statistic.group import IRepositoryGroupStatistic
from src.data.models.challenges.mission import GroupMissionModel


class GroupStatisticRepository(IRepositoryGroupStatistic):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def mission_counter(self, *, group_id: int) -> GroupMissionCounterDTO:
        stmt = select(GroupMissionModel).where(
            GroupMissionModel.group_id == group_id, GroupMissionModel.status == OccupancyStatusEnum.FINISH
        )
        result = await self.db_context.scalars(statement=stmt)
        counter = 0
        if result:
            counter = len(result.all())
        return GroupMissionCounterDTO(group_id=group_id, counter=counter)
