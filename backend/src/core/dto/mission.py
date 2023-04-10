from dataclasses import dataclass, field

from src.core.dto.occypancy import OccupancyCategoryDTO
from src.core.enum.base import RelatedEnum
from src.core.enum.occupancy import OccupancyStatusEnum


@dataclass
class CreateMissionDTO:
    name: str
    description: str
    instruction: str
    score: int
    category: OccupancyCategoryDTO
    status: OccupancyStatusEnum
    related: RelatedEnum = field(init=False)