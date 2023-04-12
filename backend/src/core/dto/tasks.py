from dataclasses import dataclass

from src.core.dto.occypancy import OccupancyCategoryDTO


@dataclass
class CreateTaskDTO:
    name: str
    description: str
    score: int
    category: OccupancyCategoryDTO


@dataclass
class UpdateTaskDTO:
    """"""
