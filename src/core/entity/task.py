from dataclasses import dataclass

from src.core.enum.language import LanguageEnum
from src.core.dto.challenges.category import OccupancyCategoryDTO
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
    category: OccupancyCategoryDTO
    translations: list[TaskTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class TaskCreateDTO(TranslationMixin):
    score: int
    category: OccupancyCategoryDTO
    translations: list[TaskTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class TaskUpdateDTO(TranslationMixin):
    id: int
    score: int | None = None
    category: OccupancyCategoryDTO | None = None
    translations: list[TaskTranslateDTO] | None = None

    def __post_init__(self):
        if isinstance(self.translations, list):
            self._validate_translations(seq=self.translations)
