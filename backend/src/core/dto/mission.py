from dataclasses import dataclass, field
from datetime import datetime

from src.core.dto.occupancy import OccupancyCategoryDTO
from src.core.enum.base import RelatedEnum
from src.core.enum.occupancy import OccupancyStatusEnum


@dataclass
class CreateMissionBaseDTO:
    name: str
    description: str
    instruction: str
    score: int
    category: OccupancyCategoryDTO
    status: OccupancyStatusEnum
    related: RelatedEnum = field(init=False)


@dataclass
class CreateMissionUserDTO:
    def __post_init__(self):
        self.related = RelatedEnum.USER


@dataclass
class CreateMissionCommunityDTO:
    author: str 
    meeting_date: datetime
    people_required: int
    people_max: int
    place: str
    comment: str

    def __post_init__(self):
        self.related = RelatedEnum.COMMUNITY


@dataclass
class UpdateMissionCommunityDTO(CreateMissionCommunityDTO):
    """ """