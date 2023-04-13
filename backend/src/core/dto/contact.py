from dataclasses import dataclass

from src.core.dto.base import TypeDTO
from src.core.enum.language import LanguageEnum
from src.core.exception.language import TranslateError


@dataclass
class ContactTypeTranslateDTO(TypeDTO):
    contact_type_id: int
    language: LanguageEnum


@dataclass
class ContactTypeTranslatedCreateDTO(TypeDTO):
    language: LanguageEnum


@dataclass
class ContactTypeCreateDTO(TypeDTO):
    """ """
    translations = list[ContactTypeTranslatedCreateDTO]

    def __post_init__(self):
        translated_contact_type = [item.language for item in self.translations]
        available_languages = [lang for lang in LanguageEnum]
        difference = set(translated_contact_type) - set(available_languages)
        if len(difference) != 0:
            raise TranslateError(languages=difference)


@dataclass
class ContactTypeDTO:
    id: int
    translations = list[ContactTypeTranslatedCreateDTO]
    valid: bool

    def __post_init__(self):
        translated_contact_type = [item.language for item in self.translations]
        available_languages = [lang for lang in LanguageEnum]
        difference = set(translated_contact_type) - set(available_languages)
        if len(difference) != 0:
            self.valid = False