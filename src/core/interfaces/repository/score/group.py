from abc import ABC, abstractmethod

from src.core.dto.group.score import AddScoreGroupDTO, GroupRatingDTO, GroupScoreDTO
from src.core.entity.score import ScoreGroup
from src.core.enum.group.privacy import GroupPrivacyEnum


class IRepositoryGroupScore(ABC):
    @abstractmethod
    async def add(self, *, obj: AddScoreGroupDTO) -> ScoreGroup:
        ...

    @abstractmethod
    async def get_score(self, *, group_id: int) -> GroupScoreDTO:
        ...

    @abstractmethod
    async def get_rating(
        self,
        *,
        group_id: int,
    ) -> GroupRatingDTO:
        ...

    @abstractmethod
    async def get_rating_window(
        self,
        *,
        window_offset: int,
        group_id: int,
        group_privacy__in: list[GroupPrivacyEnum],
    ) -> list[GroupRatingDTO]:
        ...

    @abstractmethod
    async def get_rating_top(self, *, size: int, group_privacy__in: list[GroupPrivacyEnum]) -> list[GroupRatingDTO]:
        ...
