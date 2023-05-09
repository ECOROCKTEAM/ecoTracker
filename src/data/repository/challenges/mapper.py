from typing import TypeVar
from src.core.const.translate import DEFAULT_LANGUANGE
from src.core.dto.challenges.category import OccupancyCategoryDTO
from src.core.enum.language import LanguageEnum
from src.core.exception.base import TranslateNotFound
from src.data.models.challenges.occupancy import OccupancyCategoryModel

T = TypeVar("T")


def select_translation(translations: list[T], lang: LanguageEnum) -> T:
    translation_map = {t.language: t for t in translations}  # type: ignore
    translation = translation_map.get(lang, translation_map.get(DEFAULT_LANGUANGE))
    if translation is None:
        raise TranslateNotFound(msg="")
    return translation


def category_model_to_dto(model: OccupancyCategoryModel, lang: LanguageEnum) -> OccupancyCategoryDTO:
    translation = select_translation(model.translations, lang=lang)
    return OccupancyCategoryDTO(id=model.id, name=translation.name, language=translation.language)
