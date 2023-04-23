from abc import ABC, abstractmethod

from src.core.dto.challenges.status import OccupancyStatusCreateDTO, OccupancyStatusDTO
from src.core.dto.challenges.type import OccupancyTypeCreateDTO, OccupancyTypeDTO


class IOccupancyRepository(ABC):

    @abstractmethod
    async def occupancy_status_create(self, *, obj: OccupancyStatusCreateDTO) -> OccupancyStatusDTO:
        """ Create occupancy status

        Args:
            obj (OccupancyStatusCreateDTO): DTO for creating occupancy status object

        Returns:
            OccupancyStatusDTO: DTO of occupancy status
        """

    @abstractmethod
    async def occupancy_type_create(self, *, obj: OccupancyTypeCreateDTO) -> OccupancyTypeDTO:
        """ Create occupancy type

        Args:
            obj (OccupancyTypeCreateDTO): DTO of creating occupancy type object

        Returns:
            OccupancyTypeDTO: DTO of occupancy type
        """
