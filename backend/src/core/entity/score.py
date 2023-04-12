from dataclasses import dataclass, field

from src.core.enum.base import RelatedEnum


@dataclass
class ScoreBase: 
    value: int
    related: RelatedEnum = field(init=False)


@dataclass
class ScoreUser(ScoreBase):

    def __post_init__(self):
        self.related = RelatedEnum.USER


@dataclass
class ScoreCommunity(ScoreBase):

    def __post_init__(self):
        self.related = RelatedEnum.COMMUNITY