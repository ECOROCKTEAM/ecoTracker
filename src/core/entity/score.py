from dataclasses import dataclass

from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class ScoreUser:
    user_id: int
    value: int
    operation: ScoreOperationEnum


@dataclass
class ScoreGroup:
    group_id: int
    value: int
    operation: ScoreOperationEnum
