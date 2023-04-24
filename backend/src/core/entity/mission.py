from dataclasses import dataclass, field
from typing import Optional
from src.core.dto.challenges.mission.mission import MissionCreateTranslateDTO, MissionTranslateDTO

from src.core.dto.challenges.type import OccupancyTypeDTO
from src.core.dto.challenges.status import OccupancyStatusDTO
from src.core.enum.challenges.related import RelatedEnum
from src.core.mixin.validators.translations import TranslationMixin


@dataclass
class Mission(TranslationMixin):
    id: int
    score: int
    type: OccupancyTypeDTO
    status: OccupancyStatusDTO
    translations: list[MissionTranslateDTO]
    related: RelatedEnum = field(init=False)

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class MissionCreateDTO(TranslationMixin):
    score: int
    occupancy_type_id: int
    translations: list[MissionCreateTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class MissionUpdateDTO(TranslationMixin):
    id: int
    translations: list[MissionCreateTranslateDTO]
    score: Optional[int] = None
    occupancy_type_id: Optional[int] = None

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class MissionUserCreateDTO:
    username: str
    mission_id: int
    status_id: int


@dataclass
class MissionUserUpdateDTO:
    id: int
    status_id: Optional[int] = None


@dataclass
class MisssionUser(Mission):
    id: int
    username: str

    def __post_init__(self):
        self.related = RelatedEnum.USER


@dataclass
class MissionCommunityCreateDTO:
    mission_id: int
    status_id: int
    community_id: str
    author: str
    place: Optional[str] = None
    meeting_date: Optional[int] = None
    people_required: Optional[int] = None
    people_max: Optional[int] = None
    comment: Optional[str] = None

@dataclass
class MissionCommunityUpdateDTO:
    id: int
    status_id: Optional[int] = None
    place: Optional[str] = None
    meeting_date: Optional[int] = None
    people_required: Optional[int] = None
    people_max: Optional[int] = None
    comment: Optional[str] = None

@dataclass
class MissionCommunity(Mission):
    place: Optional[str]
    meeting_date: Optional[int]
    people_required: Optional[int]
    people_max: Optional[int]
    comment: Optional[str]
    author: str  # creator user.username

    def __post_init__(self):
        self.related = RelatedEnum.COMMUNITY
