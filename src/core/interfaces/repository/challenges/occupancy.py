from abc import ABC, abstractmethod

from src.core.dto.challenges.category import (
    OccupancyCategoryDTO,
)
from src.core.enum.language import LanguageEnum


class IRepositoryOccupancyCategory(ABC):
    @abstractmethod
    async def get(self, *, id: int, lang: LanguageEnum) -> OccupancyCategoryDTO:
        """Get occupancy category

        Args:
            id (int): Id category

        Returns:
            OccupancyCategoryDTO: DTO of occupancy category
        """

    @abstractmethod
    async def lst(self, lang: LanguageEnum) -> list[OccupancyCategoryDTO]:
        """Get list of occupancy category

        Args:
            lang (LanguageEnum): Target of language

        Returns:
            list[OccupancyCategoryDTO]: list of dto occupancy category
        """
