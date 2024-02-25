from dataclasses import dataclass

from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class UserRatingDTO:
    user_id: str
    score: int
    position: int


@dataclass
class UserScoreDTO:
    user_id: str
    score: int


@dataclass
class OperationWithScoreUserDTO:
    user_id: str
    value: int
    operation: ScoreOperationEnum
