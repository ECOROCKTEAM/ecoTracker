from dataclasses import dataclass
from datetime import datetime

from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum


@dataclass
class Task:
    id: int
    score: int
    category_id: int
    name: str
    active: bool
    description: str
    language: LanguageEnum


@dataclass
class TaskUserPlan:
    user_id: str
    task_id: int


@dataclass
class TaskUser:
    id: int
    user_id: str
    task_id: int
    status: OccupancyStatusEnum
    date_start: datetime
    date_close: datetime | None  # YY.MM.DD HH:mm:SS
