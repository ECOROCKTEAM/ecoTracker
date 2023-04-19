from dataclasses import dataclass

from src.core.enum.challenges.type import OccupancyTypeEnum
from src.core.enum.application.language import LanguageEnum
from src.core.mixin.validators.translations import TranslationMixin

@dataclass
class OccupancyTypeTranslateDTO:
    id: int
    type_id: int
    name: str
    language: LanguageEnum


@dataclass
class OccupancyTypeTranslateCreateDTO:
    name: str
    language: LanguageEnum


@dataclass
class OccupancyTypeCreateDTO(TranslationMixin):
    enum: OccupancyTypeEnum
    translations: list[OccupancyTypeTranslateCreateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class OccupancyTypeDTO(TranslationMixin):
    id: int
    enum: OccupancyTypeEnum
    translations: list[OccupancyTypeTranslateCreateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)