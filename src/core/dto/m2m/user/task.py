from dataclasses import dataclass

from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class UserTaskCreateDTO:
    user_id: str
    task_id: int
    occupancy: OccupancyStatusEnum


@dataclass
class UserTaskUpdateDTO:
    id: int
    occupancy: OccupancyStatusEnum
