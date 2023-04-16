from typing import List
from dataclasses import dataclass

from src.core.enum.subscription import PeriodUnitEnum, SubscriptionTypeEnum
from src.core.enum.language import LanguageEnum
from src.core.enum.base import VariableTypeEnum
from src.core.mixin.variable_type import VariableTypeCastMixin
from src.core.typing.base import VariableValueType
from backend.src.core.exception.translate import TranslateError


@dataclass
class SubscriptionConstrainsDTO(VariableTypeCastMixin):
    name: str
    _raw_value: str
    type: VariableTypeEnum

    @property
    def value(self) -> VariableValueType:
        return self._cast_type(value=self._raw_value, to_type=self.type)

    def __repr__(self) -> str:
        return f"{self.__class__}(name={self.name}, _raw_value={self._raw_value}, type={self.type}, value={self.value})"


@dataclass
class SubscriptionListConstrainsDTO:
    name: str
    constrains: List[SubscriptionConstrainsDTO]


@dataclass
class SubscriptionTypeTranslateDTO:
    id: int
    name: str
    language: LanguageEnum


@dataclass 
class SubscriptionTypeTranslateCreateDTO:
    name: str
    language: LanguageEnum


@dataclass
class SubscriptionTypeCreateDTO:
    languages: list[SubscriptionTypeTranslateCreateDTO]

    def __post_init__(self):
        translated_subscription_types = [item.language for item in self.languages]
        available_languages = [language for language in LanguageEnum]
        diff = set(available_languages) - set(translated_subscription_types)
        if diff != 0:
            raise TranslateError(languages=diff)
        

@dataclass
class SubscriptionTypeDTO:
    id: int
    languages: list[SubscriptionListConstrainsDTO]
    available: bool

    def __post_init__(self):
        translated_subscription_types = [item.language for item in self.languages]
        available_languages = [language for language in LanguageEnum]
        diff = set(available_languages) - set(translated_subscription_types)
        if diff != 0:
            self.available = False

# Period Unit


@dataclass
class SubscriptionPeriodUnitTranslateDTO:
    unit_id: int
    name: str
    language: LanguageEnum


@dataclass
class SubscriptionPeriodUnitTranslateCreateDTO:
    name: str
    language: LanguageEnum


@dataclass
class SubscriptionPeriodUnitCreateDTO:

    value: str
    languages: list[SubscriptionPeriodUnitTranslateCreateDTO]

    def __post_init__(self):
        translated_subscription_periods = [item.language for item in self.languages]
        available_languages = [language for language in LanguageEnum]
        diff = set(available_languages) - set(translated_subscription_periods)
        if diff != 0:
            raise TranslateError
        

@dataclass
class SubscriptionPeriodUnitDTO:
    id: int
    value: str
    period_unit: PeriodUnitEnum
    languages: list[SubscriptionPeriodUnitTranslateDTO]
    valid: bool


    def __post_init__(self):
        translated_subscription_periods = [item.language for item in self.languages]
        available_languages = [language for language in LanguageEnum]
        diff = set(available_languages) - set(translated_subscription_periods)
        if diff != 0:
            self.valid = False

#Subscription Period


@dataclass
class SubscriptionPeriodTranslateDTO:
    subscription_period_id: int
    name: str
    language: LanguageEnum


@dataclass
class SubscriptionPeriodCreateTranslate:
    name: str
    language: LanguageEnum


@dataclass
class SubscriptionPeriodCreateDTO:
    value: str
    languages: list[SubscriptionPeriodCreateTranslate]

    def __post_init__(self):
        translated_subscription_periods = [item.language for item in self.languages]
        available_languages = [language for language in LanguageEnum]
        diff = set(available_languages) - set(translated_subscription_periods)
        if diff != 0:
            raise TranslateError


@dataclass
class SubscriptionPeriodDTO:
    id: int
    value: str
    unit: PeriodUnitEnum
    languages: list[SubscriptionPeriodTranslateDTO]
    valid: bool

    def __post_init__(self):
        translated_subscription_periods = [item.language for item in self.languages]
        available_languages = [language for language in LanguageEnum]
        diff = set(available_languages) - set(translated_subscription_periods)
        if diff != 0:
            self.valid = False


# Subscription DTO

@dataclass
class SubscriptionTranslateDTO:
    subscription_id: int
    name: str
    language: LanguageEnum


@dataclass
class SubscriptionTranslateCreateDTO:
    name: str
    language: LanguageEnum


@dataclass
class SubscriptionCreateDTO:
    type: SubscriptionTypeEnum
    period: PeriodUnitEnum
    languages: list[SubscriptionTranslateCreateDTO]

    def __post_init__(self):
        translated_subscription_periods = [item.language for item in self.languages]
        available_languages = [language for language in LanguageEnum]
        diff = set(available_languages) - set(translated_subscription_periods)
        if diff != 0:
            raise TranslateError
        

@dataclass
class SubscriptionDTO:
    id: int
    type: SubscriptionTypeEnum
    period: PeriodUnitEnum
    languages: list[SubscriptionTranslateDTO]

    def __post_init__(self):
        translated_subscription_periods = [item.language for item in self.languages]
        available_languages = [language for language in LanguageEnum]
        diff = set(available_languages) - set(translated_subscription_periods)
        if diff != 0:
            self.valid = False
