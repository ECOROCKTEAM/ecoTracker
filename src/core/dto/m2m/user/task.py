from dataclasses import dataclass

from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.dto.challenges.status import OccupancyStatusDTO


@dataclass
class UserTaskDTO:
    id: int
    username: str
    task_id: int
    occupancy: OccupancyStatusDTO


@dataclass
class UserTaskCreateDTO:
    username: str
    task_id: int
    occupancy: OccupancyStatusDTO


@dataclass
class UserTaskUpdateDTO:
    id: int
    occupancy: OccupancyStatusDTO
