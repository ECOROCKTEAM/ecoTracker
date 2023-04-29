from abc import abstractmethod, ABC
from typing import Optional

from src.core.dto.mock import MockObj
from src.core.dto.user.score import UserBoundOffsetDTO, UserScoreDTO


class IScoreRepository(ABC):

    @abstractmethod
    async def user_score_get(self, *, user_id: str) -> UserScoreDTO:
        """ Get score for user

        Args:
            user_id (str): user identify

        Returns:
            UserScoreDTO: DTO for user score
        """

# Return хреновый. Подумать, как выводить список пользователей с их местом в рейтинге
    @abstractmethod
    async def rating_user(
        self, *, 
        obj: Optional[UserBoundOffsetDTO] = None,
        order_obj: MockObj,
        ) -> list[dict([(int, UserScoreDTO)])]: # type: ignore
        """Get user rating

        Args:
            obj (UserBoundOffsetDTO, optional): DTO for specific user. Defaults to None. If None -> rating of all users.
            order_obj (MockObj): Order for score value 
            
        Returns:
            list[UserScore]: List of DTO user score objects
        """
