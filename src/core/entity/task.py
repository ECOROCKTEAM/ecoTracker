from dataclasses import dataclass
from datetime import date, datetime

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
    user_id: int
    task_id: int


@dataclass
class TaskUser:
    date_start: date  # YY.MM.DD
    date_close: datetime | None  # YY.MM.DD HH:mm:SS
    status: OccupancyStatusEnum
    user_id: int
    task_id: int
