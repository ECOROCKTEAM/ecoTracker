from datetime import datetime
from dataclasses import dataclass

from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class UserTaskDTO:
    id: int
    user_id: int
    task_id: int
    date_start: datetime
    status: OccupancyStatusEnum


@dataclass
class UserTaskCreateDTO:
    user_id: int
    task_id: int
    occupancy: OccupancyStatusEnum


@dataclass
class UserTaskUpdateDTO:
    id: int
    occupancy: OccupancyStatusEnum
