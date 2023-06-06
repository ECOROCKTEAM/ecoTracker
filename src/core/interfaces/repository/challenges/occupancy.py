from abc import ABC, abstractmethod

from src.core.entity.occupancy import OccupancyCategory
from src.core.enum.language import LanguageEnum


class IRepositoryOccupancyCategory(ABC):
    @abstractmethod
    async def get(self, *, id: int, lang: LanguageEnum) -> OccupancyCategory:
        """Get occupancy category

        Args:
            id (int): Id category

        Returns:
            OccupancyCategory: Occupancy category entity object
        """

    @abstractmethod
    async def lst(self, lang: LanguageEnum) -> list[OccupancyCategory]:
        """Get list of occupancy category

        Args:
            lang (LanguageEnum): Target of language

        Returns:
            list[OccupancyCategory]: list of occupancy category entity object
        """
