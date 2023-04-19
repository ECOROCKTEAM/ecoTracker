from dataclasses import dataclass

from src.core.dto.subscription.constraint import SubscriptionConstraintDTO
from src.core.enum.application.language import LanguageEnum
from src.core.mixin.validators.translations import TranslationMixin


@dataclass
class SubscriptionTypeTranslateDTO:
    id: int
    name: str
    type_id: int
    language: LanguageEnum


@dataclass
class SubscriptionTypeTranslateCreateDTO:
    name: str
    type_id: int
    language: LanguageEnum


@dataclass
class SubscriptionTypeCreateDTO(TranslationMixin):
    name: str
    translations: list[SubscriptionTypeTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class SubscriptionTypeDTO(TranslationMixin):
    id: int
    translations: list[SubscriptionTypeTranslateDTO]
    constrains: list[SubscriptionConstraintDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)
