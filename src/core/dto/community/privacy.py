from dataclasses import dataclass, field

from src.core.enum.application.language import LanguageEnum
from src.core.enum.community.privacy import PrivacyEnum
from src.core.mixin.validators.translations import TranslationMixin


@dataclass
class PrivacyTranslateDTO:
    id: int
    privacy_id: int
    name: str
    language: LanguageEnum


@dataclass
class PrivacyCreateTranslateDTO:
    name: str
    privacy_id: int
    language: LanguageEnum


@dataclass
class PrivacyCreateDTO(TranslationMixin):
    enum: PrivacyEnum
    translations: list[PrivacyCreateTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class PrivacyDTO(TranslationMixin):
    id: int
    enum: PrivacyEnum
    translations: list[PrivacyTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)
