from abc import ABC, abstractmethod

from src.core.dto.statistic.group import GroupMissionCounterDTO
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter


class IRepositoryGroupStatistic(ABC):
    @abstractmethod
    async def mission_counter(self, *, group_id: int, filter_obj: OccupancyStatisticFilter) -> GroupMissionCounterDTO:
        """Сounter of completed missions by the group

        Args:
            group_id (int): Group ID
            filter_obj (OccupancyStatisticFilter): Occupancy status filter

        Returns:
            GroupMissionCounterDTO: Group missions counter DTO
        """
