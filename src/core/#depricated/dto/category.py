##########################################################
# The data from below will be moved to admin application #
##########################################################

# from src.core.mixin.validators.translations import TranslationMixin

# @dataclass
# class OccupancyCategoryTranslateDTO:
#     id: int
#     type_id: int
#     name: str
#     language: LanguageEnum


# @dataclass
# class OccupancyCategoryTranslateCreateDTO:
#     name: str
#     language: LanguageEnum


# @dataclass
# class OccupancyCategoryCreateDTO(TranslationMixin):
#     translations: list[OccupancyCategoryTranslateCreateDTO]

#     def __post_init__(self):
#         self._validate_translations(seq=self.translations)
