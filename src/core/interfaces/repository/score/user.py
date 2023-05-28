from abc import ABC, abstractmethod

from src.core.dto.mock import MockObj
from src.core.dto.user.score import (
    OperationWithScoreUserDTO,
    UserBoundOffsetDTO,
    UserRatingDTO,
    UserScoreDTO,
)
from src.core.entity.score import ScoreUser


class IRepositoryUserScore(ABC):
    @abstractmethod
    async def user_get(self, *, user_id: int) -> UserScoreDTO:
        """Get user score

        Args:
            user_id (int): user identify

        Returns:
            UserRating: DTO of user score object
        """

    @abstractmethod
    async def user_rating(
        self,
        *,
        obj: UserBoundOffsetDTO | None = None,
        order_obj: MockObj,
    ) -> list[UserRatingDTO]:
        """Get user rating

        Args:
            obj (UserBoundOffsetDTO, optional): DTO for specific user. Defaults to None. If None -> rating of all users.
            order_obj (MockObj): Order for score value

        Returns:
            list[UserRatingDTO]: List of DTO of user score object
        """

    @abstractmethod
    async def add(self, *, obj: OperationWithScoreUserDTO) -> ScoreUser:
        """Operation with user score (addiction, subtraction, multiplication, division)

        Args:
            obj (IncrementScoreUserDTO): DTO of user object, value and math operator

        Returns:
            ScoreUser: User score entity
        """
