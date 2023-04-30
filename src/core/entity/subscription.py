from dataclasses import dataclass

from src.core.enum.language import LanguageEnum
from src.core.enum.subscription.subscription import SubscriptionTypeEnum
from src.core.dto.subscription.period import SubscriptionPeriodDTO
from src.core.mixin.validators.translations import TranslationMixin


@dataclass
class SubscriptionTranslateDTO:
    id: int
    name: str
    subscription_id: int
    language: LanguageEnum


@dataclass
class SubscriptionTranslateCreateDTO:
    name: str
    subscription_id: int
    language: LanguageEnum


@dataclass
class SubscriptionCreateDTO(TranslationMixin):
    type: SubscriptionTypeEnum
    period: SubscriptionPeriodDTO
    translations: list[SubscriptionTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class Subscription(TranslationMixin):
    id: int
    type: SubscriptionTypeEnum
    period: SubscriptionPeriodDTO
    translations: list[SubscriptionTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)
