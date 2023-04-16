from dataclasses import dataclass, field

from src.core.enum.score import ScoreOperationEnum
# from src.core.enum.base import RelatedEnum


@dataclass 
class ScoreUserDTO:
    username: str
    value: int
    operation: ScoreOperationEnum


# @dataclass
# class ScoreBaseDTO:
#     value: int
#     operation: str
#     related: RelatedEnum = field(init=False)


# @dataclass
# class ScoreCommunityDTO(ScoreBaseDTO):
#     def __post_init__(self):
#         self.related = RelatedEnum.COMMUNITY


# @dataclass
# class ScoreUserDTO(ScoreBaseDTO):
#     def __post_init__(self):
#         self.related = RelatedEnum.USER


# @dataclass
# class ScoreUserGetDTO(ScoreUserDTO):
#     """ """
