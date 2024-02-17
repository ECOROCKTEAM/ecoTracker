from abc import ABC, abstractmethod

from src.core.dto.statistic.user import MissionUserCounterDTO, TaskUserCounterDTO


class IRepositoryUserStatistic(ABC):
    @abstractmethod
    async def task_counter(self, *, user_id: str) -> TaskUserCounterDTO:
        """Сounter of completed tasks by the user

        Args:
            user_id (str): User ID

        Returns:
            TaskUserCounterDTO: User task counter DTO
        """

    @abstractmethod
    async def mission_counter(self, *, user_id: str) -> MissionUserCounterDTO:
        """Сounter of completed missions by the user

        Args:
            user_id (str):  User ID

        Returns:
            MissionUserCounterDTO: User missions counter DTO
        """
