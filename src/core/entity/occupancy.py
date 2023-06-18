from dataclasses import dataclass

from src.core.enum.language import LanguageEnum


@dataclass
class OccupancyCategory:
    id: int
    name: str
    language: LanguageEnum
