from dataclasses import dataclass


@dataclass
class GroupMissionCounterDTO:
    group_id: int
    counter: int
