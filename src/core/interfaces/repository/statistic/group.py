from abc import ABC, abstractmethod

from src.core.dto.statistic.group import GroupMissionCounterDTO


class IRepositoryGroupStatistic(ABC):
    @abstractmethod
    async def mission_counter(self, *, group_id: int) -> GroupMissionCounterDTO:
        """Сounter of completed missions by the group

        Args:
            group_id (int): Group ID

        Returns:
            GroupMissionCounterDTO: Group missions counter DTO
        """
