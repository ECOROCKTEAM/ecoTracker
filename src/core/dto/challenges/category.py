from dataclasses import dataclass

from src.core.enum.language import LanguageEnum
from src.core.mixin.validators.translations import TranslationMixin


@dataclass
class OccupancyCategoryTranslateDTO:
    id: int
    type_id: int
    name: str
    language: LanguageEnum


@dataclass
class OccupancyCategoryTranslateCreateDTO:
    name: str
    language: LanguageEnum


@dataclass
class OccupancyCategoryCreateDTO(TranslationMixin):
    translations: list[OccupancyCategoryTranslateCreateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class OccupancyCategoryDTO(TranslationMixin):
    id: int
    translations: list[OccupancyCategoryTranslateCreateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)
