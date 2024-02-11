from dataclasses import dataclass

from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class ScoreUser:
    user_id: str
    value: int
    operation: ScoreOperationEnum
    task_totaly_completed: int
    mission_totaly_completed: int


@dataclass
class ScoreGroup:
    group_id: int
    value: int
    operation: ScoreOperationEnum
    mission_totaly_completed: int
