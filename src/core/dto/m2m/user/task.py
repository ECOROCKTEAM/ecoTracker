from dataclasses import dataclass

from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class UserTaskDTO:
    id: int
    username: str
    task_id: int
    status: OccupancyStatusEnum


@dataclass
class UserTaskCreateDTO:
    username: str
    task_id: int
    occupancy: OccupancyStatusEnum


@dataclass
class UserTaskUpdateDTO:
    id: int
    occupancy: OccupancyStatusEnum
