from dataclasses import dataclass

from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class CommunityScoreDTO:
    community_id: int
    value: int
    position: int


@dataclass
class CommunityBoundOffsetDTO:
    community_id: int
    bound_offset: int


@dataclass
class CommunityOperationWithScoreDTO:
    community_id: int
    value: int
    operation: ScoreOperationEnum
