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
class UserTaskDeleteDTO:
    user_id: str
    task_id: int


@dataclass
class UserTaskCreateDTO:
    username: str
    task_id: int
    occupancy: OccupancyStatusDTO = OccupancyStatusEnum.ACTIVE


@dataclass
class UserTaskUpdateDTO:
    id: int
    occupancy: OccupancyStatusDTO
