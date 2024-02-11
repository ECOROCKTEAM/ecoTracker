from dataclasses import dataclass

from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class UserRatingDTO:
    user_id: str
    value: int
    position: int


@dataclass
class UserScoreDTO:
    user_id: str
    value: int
    task_totaly_completed: int
    mission_totaly_completed: int


@dataclass
class OperationWithScoreUserDTO:
    user_id: str
    value: int
    operation: ScoreOperationEnum
    task_totaly_completed: int | None = 0
    mission_totaly_completed: int | None = 0


@dataclass
class UserBoundOffsetDTO:
    """Number of users when sorting before and after a specific user."""

    user_id: str
    bound_offset: int
