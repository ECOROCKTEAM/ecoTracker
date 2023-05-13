from dataclasses import dataclass
from datetime import date, datetime
from src.core.enum.language import LanguageEnum
from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class Task:
    id: int
    score: int
    category_id: int
    name: str
    description: str
    language: LanguageEnum


@dataclass
class TaskUserPlan:
    id: int
    user_id: int
    task_id: int


@dataclass
class TaskUser:
    id: int
    date: date  # YY.MM.DD
    date_close: datetime | None  # YY.MM.DD HH:mm:SS
    status: OccupancyStatusEnum
    user_id: int
    task_id: int
