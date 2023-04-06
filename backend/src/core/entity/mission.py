from dataclasses import dataclass, field
from backend.src.core.dto.tasks import OccupancyCategoryDTO

from backend.src.core.enum.base import RelatedEnum
from backend.src.core.enum.category import OccupancyStatusEnum


@dataclass
class MissionBase:
    id: int
    name: str
    description: str
    instruction: str
    score: int
    author: str  # user.username
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

    def __post_init__(self):
        self.related = RelatedEnum.COMMUNITY
