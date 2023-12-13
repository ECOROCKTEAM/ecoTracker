from dataclasses import dataclass
from datetime import datetime

from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum


@dataclass
class Mission:
    """Сущность миссии"""

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
    """Сущность миссии пользователя"""

    id: int
    user_id: str
    mission_id: int
    date_start: datetime
    date_close: datetime | None
    status: OccupancyStatusEnum


@dataclass
class MissionGroup:
    """Сущность миссии сообщества"""

    id: int
    group_id: int
    mission_id: int
    author: str
    date_start: datetime
    date_close: datetime | None
    status: OccupancyStatusEnum
    place: str | None = None
    meeting_date: datetime | None = None
    people_required: int | None = None
    people_max: int | None = None
    comment: str | None = None
