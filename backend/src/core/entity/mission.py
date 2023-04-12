from dataclasses import dataclass, field

from src.core.dto.occypancy import OccupancyCategoryDTO
from src.core.enum.base import RelatedEnum
from src.core.enum.occupancy import OccupancyStatusEnum


@dataclass
class MissionBase:
    id: int
    name: str
    description: str
    instruction: str
    score: int
    category: OccupancyCategoryDTO
    status: OccupancyStatusEnum
    related: RelatedEnum = field(init=False)


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
