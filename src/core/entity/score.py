from dataclasses import dataclass

from src.core.enum.score.score import ScoreOperationEnum


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
