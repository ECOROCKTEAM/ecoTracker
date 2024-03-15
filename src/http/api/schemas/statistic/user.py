from pydantic import BaseModel

from src.core.dto.statistic.user import MissionUserCounterDTO, TaskUserCounterDTO


class UserTaskCounterSchema(BaseModel):
    user_id: str
    counter: int

    @classmethod
    def from_obj(cls, user_tasks_counter: TaskUserCounterDTO) -> "UserTaskCounterSchema":
        return UserTaskCounterSchema(user_id=user_tasks_counter.user_id, counter=user_tasks_counter.counter)


class UserMissionCounterSchema(BaseModel):
    user_id: str
    counter: int

    @classmethod
    def from_obj(cls, user_mission_counter: MissionUserCounterDTO) -> "UserMissionCounterSchema":
        return UserMissionCounterSchema(user_id=user_mission_counter.user_id, counter=user_mission_counter.counter)
