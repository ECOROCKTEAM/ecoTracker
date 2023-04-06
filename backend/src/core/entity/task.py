from dataclasses import dataclass

from backend.src.core.dto.tasks import OccupancyCategoryDTO
from backend.src.core.enum.category import OccupancyStatusEnum


@dataclass
class Task:
    id: int
    name: str
    description: str
    score: int
    category: OccupancyCategoryDTO
    status: OccupancyStatusEnum
