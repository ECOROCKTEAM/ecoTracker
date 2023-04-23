from dataclasses import dataclass

from src.core.enum.user.contact import ContactEnum
from src.core.enum.application.language import LanguageEnum
from src.core.mixin.validators.translations import TranslationMixin

# ContactType


@dataclass
class ContactTypeTranslateDTO:
    id: int
    type_id: int
    name: str
    language: LanguageEnum


@dataclass
class ContactTypeTranslatedCreateDTO:
    name: str
    type_id: int
    language: LanguageEnum


@dataclass
class ContactTypeCreateDTO(TranslationMixin):
    enum: ContactEnum
    translations: list[ContactTypeTranslatedCreateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class ContactTypeDTO(TranslationMixin):
    id: int
    enum: ContactEnum
    translations: list[ContactTypeTranslatedCreateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


# Contact


@dataclass
class ContactDTO:
    id: int
    value: str
    type: ContactTypeDTO


@dataclass
class ContactCreateDTO:
    value: str
    type: ContactTypeDTO


@dataclass
class ContactUpdateDTO:
    value: str = None
    active: bool = None
