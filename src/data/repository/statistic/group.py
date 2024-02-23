from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.statistic.group import GroupMissionCounterDTO
from src.core.interfaces.repository.statistic.group import IRepositoryGroupStatistic
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter
from src.data.models.challenges.mission import GroupMissionModel


class GroupStatisticRepository(IRepositoryGroupStatistic):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def mission_counter(self, *, group_id: int, filter_obj: OccupancyStatisticFilter) -> GroupMissionCounterDTO:
        where_clause = [GroupMissionModel.group_id == group_id]
        if filter_obj.status__in is not None:
            where_clause.append(GroupMissionModel.status.in_(filter_obj.status__in))

        stmt = select(func.count(GroupMissionModel.id)).where(*where_clause)
        (counter,) = await self.db_context.scalars(statement=stmt)

        return GroupMissionCounterDTO(group_id=group_id, counter=counter)
