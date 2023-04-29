from dataclasses import dataclass


@dataclass
class UserScoreDTO:
    username: str
    value: int


@dataclass
class UserBoundOffsetDTO:
    username: str
    bound_offset: int