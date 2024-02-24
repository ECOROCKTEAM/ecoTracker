from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.statistic.user import MissionUserCounterDTO, TaskUserCounterDTO
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter
from src.core.interfaces.repository.statistic.user import IRepositoryUserStatistic
from src.data.models.challenges.mission import UserMissionModel
from src.data.models.challenges.task import UserTaskModel


class UserStatisticRepository(IRepositoryUserStatistic):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def task_counter(self, *, user_id: str, filter_obj: OccupancyStatisticFilter) -> TaskUserCounterDTO:
        where_clause = [UserTaskModel.user_id == user_id]
        if filter_obj.status__in is not None:
            where_clause.append(UserTaskModel.status.in_(filter_obj.status__in))

        stmt = select(func.count(UserTaskModel.id)).where(*where_clause)
        counter = await self.db_context.scalar(statement=stmt)

        assert counter is not None

        return TaskUserCounterDTO(user_id=user_id, counter=counter or 0)

    async def mission_counter(self, *, user_id: str, filter_obj: OccupancyStatisticFilter) -> MissionUserCounterDTO:
        where_clause = [UserMissionModel.user_id == user_id]
        if filter_obj.status__in is not None:
            where_clause.append(UserMissionModel.status.in_(filter_obj.status__in))

        stmt = select(func.count(UserMissionModel.id)).where(*where_clause)
        counter = await self.db_context.scalar(statement=stmt)

        assert counter is not None

        return MissionUserCounterDTO(user_id=user_id, counter=counter or 0)
