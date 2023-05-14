from dataclasses import dataclass
from datetime import datetime, date

from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class TaskUserPlanCreateDTO:
    user_id: int
    task_id: int


@dataclass
class TaskUserCreateDTO:
    date: date  # YY.MM.DD, mb auto in psql?
    user_id: int
    task_id: int
    date_close: datetime | None = None
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE


@dataclass
class TaskUserUpdateDTO:
    task_id: int
    user_id: int | None = None  # Мб передавать сразу User entity, чтобы язык получать?
    date_close: datetime | None = None
    status: OccupancyStatusEnum | None = None
