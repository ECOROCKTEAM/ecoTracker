from abc import ABC, abstractmethod

from src.core.dto.community.score import (
    CommunityBoundOffsetDTO,
    CommunityOperationWithScoreDTO,
    CommunityScoreDTO,
)
from src.core.dto.mock import MockObj


class IRepositoryCommunityScore(ABC):
    @abstractmethod
    async def change(self, *, obj: CommunityOperationWithScoreDTO) -> CommunityScoreDTO:
        """Action with community score

        Args:
            obj (CommunityOperationWithScoreDTO): DTO of community object, value and math operator

        Returns:
            CommunityScoreDTO: DTO of community score object
        """

    @abstractmethod
    async def community_get(self, *, community_id: int) -> CommunityScoreDTO:
        """Get community score

        Args:
            community_id (int): community identify

        Returns:
            CommunityScoreDTO: DTO of community score object
        """

    @abstractmethod
    async def community_rating(
        self,
        *,
        order_obj: MockObj,
        obj: CommunityBoundOffsetDTO | None = None,
    ) -> dict[int, CommunityScoreDTO]:
        """Get community rating

        Args:
            order_obj (MockObj): order object
            obj (CommunityBoundOffsetDTO | None, optional): DTO of community object.
                If not None return rating for specific community with bound offset.
                If None return global community rating.
                Defaults to None.

        Returns:
            dict[int, CommunityRatingDTO]: Dict with rating position as a key and DTO community object as a value.
        """
