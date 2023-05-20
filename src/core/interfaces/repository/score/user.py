from abc import ABC, abstractmethod

from src.core.dto.mock import MockObj
from src.core.dto.user.score import (
    OperationWithScoreUserDTO,
    UserBoundOffsetDTO,
    UserScoreDTO,
)


class IRepositoryUserScore(ABC):
    @abstractmethod
    async def user_get(self, *, user_id: int) -> UserScoreDTO:
        """Get user score

        Args:
            user_id (int): user identify

        Returns:
            UserScoreDTO: DTO of user score object
        """

    @abstractmethod
    async def user_rating(
        self,
        *,
        obj: UserBoundOffsetDTO | None = None,
        order_obj: MockObj,
    ) -> dict[int, UserScoreDTO]:
        """Get user rating

        Args:
            obj (UserBoundOffsetDTO, optional): DTO for specific user. Defaults to None. If None -> rating of all users.
            order_obj (MockObj): Order for score value

        Returns:
            list[UserScore]: List of DTO user score objects
        """

    @abstractmethod
    async def user_change(self, *, obj: OperationWithScoreUserDTO) -> UserScoreDTO:
        """Operation with user score (addiction, subtraction, multiplication, division)

        Args:
            obj (IncrementScoreUserDTO): DTO of user object, value and math operator

        Returns:
            UserScoreDTO: DTO of user value object
        """