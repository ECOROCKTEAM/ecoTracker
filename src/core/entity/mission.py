from dataclasses import dataclass, field
from src.core.dto.challenges.mission.mission import MissionCreateTranslateDTO, MissionTranslateDTO

from src.core.dto.challenges.type import OccupancyTypeDTO
from src.core.dto.challenges.status import OccupancyStatusDTO
from src.core.enum.challenges.related import RelatedEnum
from src.core.mixin.validators.translations import TranslationMixin


@dataclass
class Mission(TranslationMixin):
    id: int
    active: bool
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
    active: bool | None = None
    score: int | None = None
    occupancy_type_id: int | None = None

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
    status_id: int | None = None


@dataclass
class MissionUser(Mission):
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
    place: str | None = None
    meeting_date: int | None = None
    people_required: int | None = None
    people_max: int | None = None
    comment: str | None = None


@dataclass
class MissionCommunityUpdateDTO:
    id: int
    status_id: int | None = None
    place: str | None = None
    meeting_date: int | None = None
    people_required: int | None = None
    people_max: int | None = None
    comment: str | None = None


@dataclass
class MissionCommunity(Mission):
    place: str | None
    meeting_date: int | None
    people_required: int | None
    people_max: int | None
    comment: str | None
    author: str  # creator user.username

    def __post_init__(self):
        self.related = RelatedEnum.COMMUNITY
