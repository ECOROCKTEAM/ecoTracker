from dataclasses import dataclass
from src.core.dto.base import ScoreBaseDTO

from src.core.enum.base import RelatedEnum


@dataclass
class ScoreCommunityDTO(ScoreBaseDTO):
    def __post_init__(self):
        self.related = RelatedEnum.COMMUNITY


@dataclass
class ScoreUserDTO(ScoreBaseDTO):
    def __post_init__(self):
        self.related = RelatedEnum.USER
