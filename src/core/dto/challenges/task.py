from dataclasses import dataclass
from datetime import date, datetime

from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class TaskUserPlanCreateDTO:
    user_id: int
    task_id: int


@dataclass
class TaskUserCreateDTO:
    date_start: date  # YY.MM.DD, mb auto in psql?
    task_id: int
    date_close: datetime | None = None
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE


@dataclass
class TaskUserUpdateDTO:
    date_close: datetime | None = None
    status: OccupancyStatusEnum | None = None
