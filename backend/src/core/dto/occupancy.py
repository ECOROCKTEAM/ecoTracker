from dataclasses import dataclass

from src.core.exception.language import TranslateError
from src.core.enum.language import LanguageEnum
from src.core.dto.base import TypeDTO


@dataclass
class OccupancyCategoryDTO:
    id: int
    name: str


@dataclass
class OccupancyDTO(TypeDTO):
    """"""


# Occupancy Type

@dataclass
class OccupancyTypeTranslateDTO:
    type_id: int
    name: str
    language: LanguageEnum


@dataclass
class OccupancyTypeTranslateCreateDTO:
    name: str
    language: LanguageEnum


@dataclass
class OccupancyTypeCreateDTO:
    languages: list[OccupancyTypeTranslateCreateDTO]

    def __post_init__(self):
        translated_contact_type = [item.language for item in self.translations]
        available_languages = [lang for lang in LanguageEnum]
        difference = set(translated_contact_type) - set(available_languages)
        if len(difference) != 0:
            raise TranslateError(languages=difference)
        

@dataclass
class OccupancyTypeDTO:
    id: int
    languages: list[OccupancyTypeTranslateCreateDTO]
    valid: bool

    def __post_init__(self):
        translated_contact_types = [item.language for item in self.translations]
        available_languages = [lang for lang in LanguageEnum]
        difference = set(translated_contact_types) - set(available_languages)
        if len(difference) != 0:
            self.valid = False


# Occupancy Status

@dataclass 
class OccupancyStatusTranslateDTO:
    status_id: int
    name: str
    language: LanguageEnum


@dataclass
class OccupancyStatusTranslateCreateDTO:
    name: str
    language: LanguageEnum


@dataclass
class OccupancyStatusCreateDTO:
    languages: list[LanguageEnum]

    def __post_init__(self):
        translated_contact_type = [item.language for item in self.translations]
        available_languages = [lang for lang in LanguageEnum]
        difference = set(translated_contact_type) - set(available_languages)
        if len(difference) != 0:
            raise TranslateError(languages=difference)
        

@dataclass
class OccupancyStatusDTO:
        id: int
        languages: list[LanguageEnum]
        valid: bool
        
        def __post_init__(self):
            translated_contact_types = [item.language for item in self.translations]
            available_languages = [lang for lang in LanguageEnum]
            difference = set(translated_contact_types) - set(available_languages)
            if len(difference) != 0:
                self.valid = False


