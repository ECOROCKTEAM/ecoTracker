from abc import ABC, abstractmethod

from src.core.dto.user.score import AddScoreUserDTO, UserRatingDTO, UserScoreDTO
from src.core.entity.score import ScoreUser


class IRepositoryUserScore(ABC):
    @abstractmethod
    async def get_score(self, *, user_id: str) -> UserScoreDTO:
        ...

    @abstractmethod
    async def get_rating(
        self,
        *,
        user_id: str,
    ) -> UserRatingDTO:
        ...

    @abstractmethod
    async def get_rating_window(
        self,
        *,
        window_offset: int,
        user_id: str,
    ) -> list[UserRatingDTO]:
        ...

    @abstractmethod
    async def get_rating_top(self, *, size: int) -> list[UserRatingDTO]:
        ...

    @abstractmethod
    async def add(self, *, obj: AddScoreUserDTO) -> ScoreUser:
        ...
