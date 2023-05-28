from dataclasses import dataclass

from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class UserRatingDTO:
    user_id: int
    value: int
    position: int


@dataclass
class UserScoreDTO:
    user_id: int
    value: int


@dataclass
class OperationWithScoreUserDTO:
    user_id: int
    value: int
    operation: ScoreOperationEnum


@dataclass
class UserBoundOffsetDTO:
    """Number of users when sorting before and after a specific user."""

    user_id: int
    bound_offset: int
