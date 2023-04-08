from dataclasses import dataclass

from src.core.dto.tasks import OccupancyCategoryDTO
from backend.src.core.enum.occupancy import OccupancyStatusEnum


@dataclass
class Task:
    id: int
    name: str
    description: str
    score: int
    category: OccupancyCategoryDTO
    status: OccupancyStatusEnum
