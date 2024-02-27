from pydantic import BaseModel

from src.core.dto.statistic.group import GroupMissionCounterDTO


class GroupMissionCounterSchema(BaseModel):
    group_id: int
    counter: int

    @classmethod
    def from_obj(cls, group_mission_counter: GroupMissionCounterDTO) -> "GroupMissionCounterSchema":
        return GroupMissionCounterSchema(group_id=group_mission_counter.group_id, counter=group_mission_counter.counter)
