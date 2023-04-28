from dataclasses import dataclass

from src.core.enum.application.language import LanguageEnum
from src.core.enum.subscription import PeriodUnitEnum
from src.core.mixin.validators.translations import TranslationMixin


@dataclass
class SubscriptionPeriodUnitTranslateDTO:
    id: int
    unit_id: int
    name: str
    language: LanguageEnum


@dataclass
class SubscriptionPeriodUnitTranslateCreateDTO:
    name: str
    language: LanguageEnum


@dataclass
class SubscriptionPeriodUnitCreateDTO(TranslationMixin):
    name: str
    translations: list[SubscriptionPeriodUnitTranslateCreateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class SubscriptionPeriodUnitDTO(TranslationMixin):
    id: int
    enum: PeriodUnitEnum
    translations: list[SubscriptionPeriodUnitTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)
