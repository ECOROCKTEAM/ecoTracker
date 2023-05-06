from dataclasses import dataclass
from datetime import date, datetime
from src.core.enum.language import LanguageEnum
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.dto.challenges.category import OccupancyCategoryDTO


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
    username: str
    task_id: int


@dataclass
class TaskUser:
    id: int
    date: date  # YY.MM.DD
    date_close: datetime | None  # YY.MM.DD HH:mm:SS
    status: OccupancyStatusEnum
    username: str
    task_id: int
