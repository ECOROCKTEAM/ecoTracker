from dataclasses import dataclass


@dataclass
class UserScoreDTO:
    user_id: int
    value: int


@dataclass
class UserBoundOffsetDTO:
    """Number of users when sorting before and after a specific user."""

    user_id: int
    bound_offset: int
