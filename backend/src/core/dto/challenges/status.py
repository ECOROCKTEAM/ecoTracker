from dataclasses import dataclass

from src.core.enum.language import LanguageEnum
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.mixin.validators.translations import TranslationMixin


@dataclass
class OccupancyStatusTranslateDTO:
    id: int
    status_id: int
    name: str
    language: LanguageEnum


@dataclass
class OccupancyStatusTranslateCreateDTO:
    name: str
    language: LanguageEnum


@dataclass
class OccupancyStatusCreateDTO(TranslationMixin):
    enum: OccupancyStatusEnum
    translations: list[OccupancyStatusTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class OccupancyStatusDTO(TranslationMixin):
    id: int
    enum: OccupancyStatusEnum
    translations: list[OccupancyStatusTranslateCreateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)
