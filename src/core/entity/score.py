from dataclasses import dataclass

from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class ScoreUserDTO:
    user_id: int
    value: int
    operation: ScoreOperationEnum


@dataclass
class ScoreCommunityDTO:
    community_name: int
    value: int
    operation: ScoreOperationEnum
