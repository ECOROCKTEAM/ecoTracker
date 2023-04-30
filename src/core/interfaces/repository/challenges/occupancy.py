from abc import ABC, abstractmethod

from src.core.dto.challenges.category import (
    OccupancyCategoryCreateDTO,
    OccupancyCategoryDTO,
)


class IOccupancyRepository(ABC):
    @abstractmethod
    async def type_create(self, *, obj: OccupancyCategoryCreateDTO) -> OccupancyCategoryDTO:
        """Create occupancy type

        Args:
            obj (OccupancyTypeCreateDTO): DTO of creating occupancy type object

        Returns:
            OccupancyTypeDTO: DTO of occupancy type
        """
