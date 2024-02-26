from pydantic import BaseModel

from src.core.dto.statistic.group import GroupMissionCounterDTO


class GroupFinishedMissionsSchema(BaseModel):
    group_id: int
    counter: int

    @classmethod
    def from_obj(cls, group_mission_counter: GroupMissionCounterDTO) -> "GroupFinishedMissionsSchema":
        return GroupFinishedMissionsSchema(
            group_id=group_mission_counter.group_id, counter=group_mission_counter.counter
        )
