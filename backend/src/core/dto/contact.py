from dataclasses import dataclass

from src.core.enum.contact import ContactEnum
from src.core.dto.base import TypeDTO
from src.core.enum.language import LanguageEnum
from backend.src.core.exception.translate import TranslateError


#Contact Type

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
        used_language = [item.language for item in self.translations]
        available_languages = [lang for lang in LanguageEnum]
        difference = set(used_language) - set(available_languages)
        if len(difference) != 0:
            raise TranslateError(languages=difference)


@dataclass
class ContactTypeDTO:
    id: int
    translations = list[ContactTypeTranslatedCreateDTO]
    valid: bool

    def __post_init__(self):
        used_languages = [item.language for item in self.translations]
        available_languages = [lang for lang in LanguageEnum]
        difference = set(used_languages) - set(available_languages)
        if len(difference) != 0:
            self.valid = False


# Contact

@dataclass
class ContactDTO:
    value: str
    type: ContactEnum


@dataclass
class ContactCreateDTO:
    value: str
    type: ContactEnum


@dataclass
class ContactDeleteDTO(ContactCreateDTO):
    """"""


@dataclass
class ContactUpdateDTO(ContactCreateDTO):
    """"""

@dataclass
class ContactUserUpdateDTO:
    username: str
    updating_contact_id: str
    contact: str
    type: ContactEnum