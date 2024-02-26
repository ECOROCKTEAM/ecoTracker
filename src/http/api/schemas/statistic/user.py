from pydantic import BaseModel

from src.core.dto.statistic.user import MissionUserCounterDTO, TaskUserCounterDTO


class UserTasksFinishedSchema(BaseModel):
    user_id: str
    counter: int

    @classmethod
    def from_obj(cls, user_tasks_counter: TaskUserCounterDTO) -> "UserTasksFinishedSchema":
        return UserTasksFinishedSchema(user_id=user_tasks_counter.user_id, counter=user_tasks_counter.counter)


class UserMissionsFinishedSchema(BaseModel):
    user_id: str
    counter: int

    @classmethod
    def from_obj(cls, user_mission_counter: MissionUserCounterDTO) -> "UserMissionsFinishedSchema":
        return UserMissionsFinishedSchema(user_id=user_mission_counter.user_id, counter=user_mission_counter.counter)
