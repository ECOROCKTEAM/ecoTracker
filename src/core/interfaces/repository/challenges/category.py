from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.entity.occupancy import OccupancyCategory
from src.core.enum.language import LanguageEnum


@dataclass
class OccupancyFilter:
    id__in: list[int] | None = None


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
    async def lst(self, lang: LanguageEnum, fltr: OccupancyFilter) -> list[OccupancyCategory]:
        """Get list of occupancy category

        Args:
            lang (LanguageEnum): Target of language
            fltr (OccupancyFilter): Occupancy filter

        Returns:
            list[OccupancyCategory]: list of occupancy category entity object
        """
