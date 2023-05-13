from dataclasses import dataclass
from datetime import date, datetime

from src.core.dto.challenges.category import OccupancyCategoryDTO
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum


@dataclass
class Task:
    id: int
    score: int
    category: OccupancyCategoryDTO
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
