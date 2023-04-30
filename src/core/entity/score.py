from dataclasses import dataclass

from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class ScoreUserDTO:
    username: str
    value: int
    operation: ScoreOperationEnum


@dataclass
class ScoreCommunityDTO:
    username: str
    value: int
    operation: ScoreOperationEnum
