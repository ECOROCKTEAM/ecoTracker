from dataclasses import dataclass

from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class GroupRatingDTO:
    group_id: int
    score: int
    position: int


@dataclass
class GroupScoreDTO:
    group_id: int
    score: int


@dataclass
class AddScoreGroupDTO:
    group_id: int
    value: int
    operation: ScoreOperationEnum
