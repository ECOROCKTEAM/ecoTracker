from dataclasses import dataclass

from src.core.enum.subscription.subscription import PeriodUnitEnum
from src.core.dto.subscription.period_unit import SubscriptionPeriodUnitDTO
from src.core.enum.application.language import LanguageEnum
from src.core.mixin.validators.translations import TranslationMixin


@dataclass
class SubscriptionPeriodTranslateDTO:
    id: int
    period_id: int
    name: str
    language: LanguageEnum


@dataclass
class SubscriptionPeriodTranslateDTO:
    name: str
    period_id: int
    language: LanguageEnum


@dataclass
class SubscriptionPeriodCreateDTO(TranslationMixin):
    value: str
    enum: PeriodUnitEnum
    translations: list[SubscriptionPeriodTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class SubscriptionPeriodDTO(TranslationMixin):
    id: int
    value: str
    enum: PeriodUnitEnum
    translations: list[SubscriptionPeriodTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)