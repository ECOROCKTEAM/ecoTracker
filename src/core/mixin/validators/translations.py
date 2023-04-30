from dataclasses import dataclass

from src.core.enum.language import LanguageEnum
from src.core.exception.translate import TranslateError


@dataclass
class TranslationMixin:
    def _validate_translations(self, seq: list):
        used_language = [item.language for item in seq]
        current_languages = [lang for lang in LanguageEnum]
        diff = set(current_languages) - set(used_language)
        if len(diff) != 0:
            raise TranslateError(languages=diff)
