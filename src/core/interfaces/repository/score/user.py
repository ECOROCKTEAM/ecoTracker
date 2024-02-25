from abc import ABC, abstractmethod

from src.core.dto.user.score import (
    OperationWithScoreUserDTO,
    UserRatingDTO,
    UserScoreDTO,
)
from src.core.entity.score import ScoreUser


class IRepositoryUserScore(ABC):
    @abstractmethod
    async def get_score(self, *, user_id: str) -> UserScoreDTO:
        """Get user score

        Args:
            user_id (str): user identify

        Returns:
            UserRating: DTO of user score object
        """

    @abstractmethod
    async def get_rating(
        self,
        *,
        user_id: str,
    ) -> UserRatingDTO:
        """Get user rating

        Args:
            user_id (int, optional): If None -> rating of all users. Defaults to None.
            order_obj (MockObj): Order for score value

        Returns:
            UserRatingDTO: User score object
        """  # noqa: E501

    @abstractmethod
    async def get_rating_window(
        self,
        *,
        size: int,
        user_id: str | None = None,
    ) -> list[UserRatingDTO]:
        """_summary_

        Args:
            user_id (int, optional): If None -> rating of all users. Defaults to None.

        Returns:
            list[UserRatingDTO]: List
        """

    @abstractmethod
    async def add(self, *, obj: OperationWithScoreUserDTO) -> ScoreUser:
        """Operation with user score (addiction, subtraction, multiplication, division)

        Args:
            obj (IncrementScoreUserDTO): DTO of user object, value and math operator

        Returns:
            ScoreUser: User score entity
        """
