from dataclasses import dataclass

from src.core.enum.application.language import LanguageEnum
from src.core.exception.translate import TranslateError


@dataclass
class MissionTranslateDTO:
    translate_id: int
    name: str
    description: str
    instruction: str
    language: LanguageEnum


@dataclass
class MissionCreateTranslateDTO:
    name: str
    description: str
    instruction: str
    language: LanguageEnum


# @dataclass
# class MissionDTO:
#     id: int
#     score: int
#     occupancy_id: int
#     translations: list[MissionCreateTranslateDTO]
#     valid: bool = True

#     def __post_init__(self):
#         used_language = [item.language for item in self.translations]
#         current_languages = [l for l in LanguageEnum]
#         diff = set(current_languages) - set(used_language)
#         if len(diff) != 0:
#             self.valid = False
