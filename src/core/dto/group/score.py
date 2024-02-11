from dataclasses import dataclass

from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class GroupRatingDTO:
    group_id: int
    value: int
    position: int


@dataclass
class GroupScoreDTO:
    group_id: int
    value: int
    mission_totaly_completed: int


@dataclass
class GroupBoundOffsetDTO:
    group_id: int
    bound_offset: int


@dataclass
class GroupOperationWithScoreDTO:
    group_id: int
    value: int
    operation: ScoreOperationEnum
    mission_totaly_completed: int
