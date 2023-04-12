from dataclasses import dataclass

from src.core.enum.language import LanguageEnum
from src.core.exception.translate import TranslateError


@dataclass
class CommunityRoleForLanguageDTO:
    translate_id: int
    name: str
    language: LanguageEnum


@dataclass
class CommunityRoleCreateForLanguageDTO:
    name: str
    language: LanguageEnum


@dataclass
class CommunityRoleCreateDTO:
    translations: list[CommunityRoleCreateForLanguageDTO]

    def __post_init__(self):
        used_language = [item.language for item in self.translations]
        current_languages = [l for l in LanguageEnum]
        diff = set(current_languages) - set(used_language)
        if len(diff) != 0:
            raise TranslateError(languages=diff)


@dataclass
class CommunityRoleDTO:
    id: int
    translations: list[CommunityRoleForLanguageDTO]
    valid: bool = True

    def __post_init__(self):
        used_language = [item.language for item in self.translations]
        current_languages = [l for l in LanguageEnum]
        diff = set(current_languages) - set(used_language)
        if len(diff) != 0:
            self.valid = False
