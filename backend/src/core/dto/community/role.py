from dataclasses import dataclass

from src.core.enum.community.role import CommunityRoleEnum
from src.core.enum.language import LanguageEnum
from src.core.mixin.validators.translations import TranslationMixin


@dataclass
class CommunityRoleTranslateDTO:
    id: int
    role_id: int
    name: str
    language: LanguageEnum


@dataclass
class CommunityRoleCreateTranslateDTO:
    name: str
    language: LanguageEnum


@dataclass
class CommunityRoleCreateDTO(TranslationMixin):
    enum: CommunityRoleEnum
    translations: list[CommunityRoleCreateTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)


@dataclass
class CommunityRoleDTO(TranslationMixin):
    id: int
    enum: CommunityRoleEnum
    translations: list[CommunityRoleTranslateDTO]

    def __post_init__(self):
        self._validate_translations(seq=self.translations)
