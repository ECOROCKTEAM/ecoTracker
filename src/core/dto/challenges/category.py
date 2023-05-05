from dataclasses import dataclass

from src.core.enum.language import LanguageEnum


@dataclass
class OccupancyCategoryDTO:
    id: int
    name: str
    language: LanguageEnum
