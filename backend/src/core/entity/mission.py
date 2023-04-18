from dataclasses import dataclass, field
from src.core.dto.challenges.mission.mission import MissionCreateTranslateDTO

from src.core.dto.challenges.type import OccupancyTypeDTO
from src.core.dto.challenges.status import OccupancyStatusDTO
from src.core.enum.challenges.related import RelatedEnum
from src.core.mixin.validators.translations import TranslationMixin


@dataclass
class MissionBase:
    id: int
    name: str
    description: str
    instruction: str
    score: int
    type: OccupancyTypeDTO
    status: OccupancyStatusDTO
    related: RelatedEnum = field(init=False)


@dataclass
class MissionBaseCreateDTO(TranslationMixin):
    score: int
    occupancy_type_id: int
    translations: list[MissionCreateTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class MisssionUser(MissionBase):
    def __post_init__(self):
        self.related = RelatedEnum.USER


@dataclass
class MissionCommunity(MissionBase):
    place: str
    meeting_date: int
    people_required: int
    people_max: int
    comment: str
    author: str  # user.username

    def __post_init__(self):
        self.related = RelatedEnum.COMMUNITY
