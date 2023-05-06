from dataclasses import dataclass
from datetime import datetime, date

from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class TaskUserPlanCreateDTO:
    username: str
    task_id: int


@dataclass
class TaskUserCreateDTO:
    date: date  # YY.MM.DD, mb auto in psql?
    username: str
    task_id: int
    date_close: datetime | None = None
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE


@dataclass
class TaskUserUpdateDTO:
    id: int
    date_close: datetime | None = None
    status: OccupancyStatusEnum | None = None
