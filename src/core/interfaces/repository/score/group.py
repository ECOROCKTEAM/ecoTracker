from abc import ABC, abstractmethod

from src.core.dto.group.score import (
    GroupBoundOffsetDTO,
    GroupOperationWithScoreDTO,
    GroupRatingDTO,
    GroupScoreDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.score import ScoreGroup


class IRepositoryGroupScore(ABC):
    @abstractmethod
    async def add(self, *, obj: GroupOperationWithScoreDTO) -> ScoreGroup:
        """Action with group score

        Args:
            obj (GroupOperationWithScoreDTO): DTO of group object, value and math operator

        Returns:
            ScoreGroup: Entity of group score object
        """

    @abstractmethod
    async def group_get(self, *, group_id: int) -> GroupScoreDTO:
        """Get group score

        Args:
            group_id (int): group identify

        Returns:
            GroupScoreDTO: DTO of group score object
        """

    @abstractmethod
    async def group_rating(
        self,
        *,
        order_obj: MockObj,
        obj: GroupBoundOffsetDTO | None = None,
    ) -> list[GroupRatingDTO]:
        """Get group rating

        Args:
            order_obj (MockObj): order object
            obj (GroupBoundOffsetDTO | None, optional): DTO of group object.
                If not None return rating for specific group with bound offset.
                If None return global group rating.
                Defaults to None.

        Returns:
            list[GroupRatingDTO]: List of DTO group score objects.
        """
