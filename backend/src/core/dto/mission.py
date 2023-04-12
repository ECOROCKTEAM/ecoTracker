from dataclasses import dataclass, field

from src.core.dto.occypancy import OccupancyCategoryDTO
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
class CreateMissionUserDTO(CreateMissionBaseDTO):
    def __post_init__(self):
        self.related = RelatedEnum.USER


@dataclass
class CreateMissionCommunityDTO(CreateMissionBaseDTO):
    def __post_init__(self):
        self.related = RelatedEnum.COMMUNITY