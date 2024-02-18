from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.statistic.user import MissionUserCounterDTO, TaskUserCounterDTO
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.interfaces.repository.statistic.user import IRepositoryUserStatistic
from src.data.models.challenges.mission import UserMissionModel
from src.data.models.challenges.task import UserTaskModel


class UserStatisticRepository(IRepositoryUserStatistic):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def task_counter(self, *, user_id: str) -> TaskUserCounterDTO:
        stmt = select(UserTaskModel).where(
            UserTaskModel.status == OccupancyStatusEnum.FINISH, UserTaskModel.user_id == user_id
        )
        result = await self.db_context.scalars(statement=stmt)
        counter = 0
        if result:
            counter = len(result.all())

        return TaskUserCounterDTO(user_id=user_id, counter=counter)

    async def mission_counter(self, *, user_id: str) -> MissionUserCounterDTO:
        stmt = select(UserMissionModel).where(
            UserMissionModel.user_id == user_id, UserMissionModel.status == OccupancyStatusEnum.FINISH
        )
        result = await self.db_context.scalars(statement=stmt)
        counter = 0
        if result:
            counter = len(result.all())

        return MissionUserCounterDTO(user_id=user_id, counter=counter)
