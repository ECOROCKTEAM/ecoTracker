from dataclasses import dataclass

from backend.src.core.exception.translate import TranslateError
from src.core.enum.language import LanguageEnum
from src.core.dto.occupancy import OccupancyCategoryDTO


@dataclass
class CreateTaskDTO:
    name: str
    description: str
    score: int
    category: OccupancyCategoryDTO


@dataclass
class TaskUpdateDTO:
    """"""

@dataclass
class TaskGetDTO:
    """"""


@dataclass
class TaskTranslateDTO:
    task_id: int
    name: str
    desc: str
    language: LanguageEnum


@dataclass
class TaskTranslateCreateDTO:
    name: str
    desc: str
    language: LanguageEnum


@dataclass
class TaskCreateDTO:
    score: int
    languages: list[TaskTranslateCreateDTO]

    def __post_init__(self):
        used_language = [item.language for item in self.translations]
        available_languages = [lang for lang in LanguageEnum]
        difference = set(used_language) - set(available_languages)
        if len(difference) != 0:
            raise TranslateError(languages=difference)
        

@dataclass
class TaskDTO:
    id: int
    score: int
    languages: list[TaskTranslateDTO]
    valid: bool

    def __post_init__(self):
        used_languages = [item.language for item in self.translations]
        available_languages = [lang for lang in LanguageEnum]
        difference = set(used_languages) - set(available_languages)
        if len(difference) != 0:
            self.valid = False