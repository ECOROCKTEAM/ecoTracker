from dataclasses import dataclass
from datetime import datetime
from src.core.enum.language import LanguageEnum
from src.core.dto.challenges.category import OccupancyCategoryDTO
from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class Mission:
    id: int
    name: str
    active: bool
    score: int
    description: str
    instruction: str
    category: OccupancyCategoryDTO
    language: LanguageEnum


@dataclass
class MissionUser:
    id: int
    status: OccupancyStatusEnum
    username: str
    mission_id: int


@dataclass
class MissionCommunity:
    id: int
    author: str
    place: str | None = None
    meeting_date: datetime | None = None
    people_required: int | None = None
    people_max: int | None = None
    comment: str | None = None
    status: OccupancyStatusEnum
    community_id: str
    mission_id: int
