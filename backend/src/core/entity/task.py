from dataclasses import dataclass

from core.dto.occupancy import OccupancyCategoryDTO
from src.core.enum.occupancy import OccupancyStatusEnum


@dataclass
class Task:
    id: int
    name: str
    description: str
    score: int
    category: OccupancyCategoryDTO
    status: OccupancyStatusEnum
