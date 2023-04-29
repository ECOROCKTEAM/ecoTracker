from dataclasses import dataclass

from src.core.enum.application.language import LanguageEnum
from src.core.dto.challenges.type import OccupancyTypeDTO
from src.core.mixin.validators.translations import TranslationMixin


@dataclass
class TaskTranslateDTO:
    id: int
    name: str
    description: str
    language: LanguageEnum


@dataclass
class TaskTranslateCreateDTO:
    name: str
    description: str
    language: LanguageEnum


@dataclass
class TaskTranslateUpdateDTO:
    id: int
    language: LanguageEnum
    name: str | None = None
    description: str | None = None


@dataclass
class Task(TranslationMixin):
    id: int
    score: int
    type: OccupancyTypeDTO
    translations: list[TaskTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class TaskCreateDTO(TranslationMixin):
    score: int
    type: OccupancyTypeDTO
    translations: list[TaskTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class TaskUpdateDTO(TranslationMixin):
    id: int
    score: int | None = None
    type: OccupancyTypeDTO | None = None
    translations: list[TaskTranslateDTO] | None = None

    def __post_init__(self):
        if isinstance(self.translations, list):
            self._validate_translations(seq=self.translations)
