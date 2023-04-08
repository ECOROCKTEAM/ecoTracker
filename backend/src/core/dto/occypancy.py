from dataclasses import dataclass

from src.core.dto.base import TypeDTO


@dataclass
class OccupancyCategoryDTO:
    id: int
    name: str


@dataclass
class OccupancyDTO(TypeDTO):
    """"""
