from dataclasses import dataclass
from backend.src.core.dto.base import ScoreBaseDTO

from backend.src.core.enum.base import RelatedEnum


@dataclass
class ScoreCommunityDTO(ScoreBaseDTO):
    def __post_init__(self):
        self.related = RelatedEnum.COMMUNITY
