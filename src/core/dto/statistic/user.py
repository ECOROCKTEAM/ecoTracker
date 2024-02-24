from dataclasses import dataclass


@dataclass
class MissionUserCounterDTO:
    user_id: str
    counter: int


@dataclass
class TaskUserCounterDTO:
    user_id: str
    counter: int
