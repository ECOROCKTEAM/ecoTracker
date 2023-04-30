from dataclasses import dataclass

from src.core.dto.challenges.mission.mission import MissionCreateTranslateDTO, MissionTranslateDTO
from src.core.dto.challenges.category import OccupancyCategoryDTO
from src.core.mixin.validators.translations import TranslationMixin
from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class MissionBase(TranslationMixin):
    id: int
    active: bool
    score: int
    category: OccupancyCategoryDTO
    translations: list[MissionTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class MissionCreateDTO(TranslationMixin):
    score: int
    category_id: int
    translations: list[MissionCreateTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class MissionUpdateDTO(TranslationMixin):
    id: int
    translations: list[MissionCreateTranslateDTO]
    active: bool | None = None
    score: int | None = None
    category_id: int | None = None

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class MissionUserCreateDTO:
    username: str
    mission_id: int
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE


@dataclass
class MissionUserUpdateDTO:
    id: int
    status: OccupancyStatusEnum | None = None


@dataclass
class MissionUser(MissionBase):
    id: int
    username: str
    status: OccupancyStatusEnum


@dataclass
class MissionCommunityCreateDTO:
    mission_id: int
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE
    community_id: str
    author: str
    place: str | None = None
    meeting_date: int | None = None
    people_required: int | None = None
    people_max: int | None = None
    comment: str | None = None


@dataclass
class MissionCommunityUpdateDTO:
    id: int
    status: OccupancyStatusEnum | None = None
    place: str | None = None
    meeting_date: int | None = None
    people_required: int | None = None
    people_max: int | None = None
    comment: str | None = None


@dataclass
class MissionCommunity(MissionBase):
    place: str | None
    meeting_date: int | None
    people_required: int | None
    people_max: int | None
    comment: str | None
    author: str  # creator user.username
    status: OccupancyStatusEnum
