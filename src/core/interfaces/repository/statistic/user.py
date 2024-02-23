from abc import ABC, abstractmethod

from src.core.dto.statistic.user import MissionUserCounterDTO, TaskUserCounterDTO
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter


class IRepositoryUserStatistic(ABC):
    @abstractmethod
    async def task_counter(self, *, user_id: str, filter_obj: OccupancyStatisticFilter) -> TaskUserCounterDTO:
        """Сounter of completed tasks by the user

        Args:
            user_id (str): User ID
            filter_obj (OccupancyStatisticFilter): Occupancy status filter

        Returns:
            TaskUserCounterDTO: User task counter DTO
        """

    @abstractmethod
    async def mission_counter(self, *, user_id: str, filter_obj: OccupancyStatisticFilter) -> MissionUserCounterDTO:
        """Сounter of completed missions by the user

        Args:
            user_id (str):  User ID
            filter_obj (OccupancyStatisticFilter): Occupancy status filter

        Returns:
            MissionUserCounterDTO: User missions counter DTO
        """
