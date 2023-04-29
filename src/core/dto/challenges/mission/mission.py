from dataclasses import dataclass

from src.core.enum.application.language import LanguageEnum


@dataclass
class MissionTranslateDTO:
    id: int
    mission_id: int
    name: str
    description: str
    instruction: str
    language: LanguageEnum


@dataclass
class MissionCreateTranslateDTO:
    mission_id: int
    name: str
    description: str
    instruction: str
    language: LanguageEnum
