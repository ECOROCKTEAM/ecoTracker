from dataclasses import dataclass
from datetime import datetime
from src.core.enum.language import LanguageEnum
from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class Mission:
    id: int
    name: str
    active: bool
    score: int
    description: str
    instruction: str
    category_id: int
    language: LanguageEnum


@dataclass
class MissionUser:
    id: int
    status: OccupancyStatusEnum
    user_id: int
    mission_id: int


@dataclass
class MissionCommunity:
    id: int
    author: str
    status: OccupancyStatusEnum
    community_id: int
    mission_id: int
    place: str | None = None
    meeting_date: datetime | None = None
    people_required: int | None = None
    people_max: int | None = None
    comment: str | None = None
