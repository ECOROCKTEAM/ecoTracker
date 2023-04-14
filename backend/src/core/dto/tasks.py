from dataclasses import dataclass

from src.core.exception.language import TranslateError
from src.core.enum.language import LanguageEnum
from src.core.dto.occupancy import OccupancyCategoryDTO


@dataclass
class CreateTaskDTO:
    name: str
    description: str
    score: int
    category: OccupancyCategoryDTO


@dataclass
class UpdateTaskDTO:
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
        translated_contact_type = [item.language for item in self.translations]
        available_languages = [lang for lang in LanguageEnum]
        difference = set(translated_contact_type) - set(available_languages)
        if len(difference) != 0:
            raise TranslateError(languages=difference)
        

@dataclass
class TaskDTO:
    id: int
    score: int
    languages: list[TaskTranslateCreateDTO]
    valid: bool

    def __post_init__(self):
        translated_contact_types = [item.language for item in self.translations]
        available_languages = [lang for lang in LanguageEnum]
        difference = set(translated_contact_types) - set(available_languages)
        if len(difference) != 0:
            self.valid = False