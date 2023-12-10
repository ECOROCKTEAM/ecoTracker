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


@dataclass
class OperationWithScoreUserDTO:
    user_id: str
    value: int
    operation: ScoreOperationEnum


@dataclass
class UserBoundOffsetDTO:
    """Number of users when sorting before and after a specific user."""

    user_id: str
    bound_offset: int
