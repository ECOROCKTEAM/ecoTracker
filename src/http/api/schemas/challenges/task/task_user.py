from fastapi import Query
from pydantic import BaseModel

from src.core.entity.task import TaskUser
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.utils import SortType
from src.core.interfaces.repository.challenges.task import (
    SortUserTaskObj,
    TaskUserFilter,
)


class SortUserTaskSchema(BaseModel):
    sort_field: str = Query(default="task_id")
    sort_type: SortType = Query(default=SortType.DESC)

    def to_obj(self) -> SortUserTaskObj:
        return SortUserTaskObj(
            field=self.sort_field,
            type=self.sort_type,
        )


class TaskUserFilterSchema(BaseModel):
    task_id: int | None = Query(default=None)
    task_active: bool | None = Query(default=None)
    status: OccupancyStatusEnum | None = Query(default=None)

    def to_obj(self) -> TaskUserFilter:
        return TaskUserFilter(
            task_id=self.task_id,
            task_active=self.task_active,
            status=self.status,
        )


class TaskUserSchema(BaseModel):
    id: int
    user_id: str
    task_id: int
    status: OccupancyStatusEnum
    date_start: int
    date_close: int | None

    @classmethod
    def from_obj(cls, task_user: TaskUser) -> "TaskUserSchema":
        return TaskUserSchema(
            id=task_user.id,
            user_id=task_user.user_id,
            task_id=task_user.task_id,
            status=task_user.status,
            date_start=int(task_user.date_start.timestamp()),
            date_close=None if task_user.date_close is None else int(task_user.date_close.timestamp()),
        )


class TaskUserListSchema(BaseModel):
    items: list[TaskUserSchema]
    limit: int | None
    offset: int
    total: int

    @classmethod
    def from_obj(
        cls, task_user_list: list[TaskUser], limit: int | None, offset: int, total: int
    ) -> "TaskUserListSchema":
        items = [TaskUserSchema.from_obj(task_user=task_user) for task_user in task_user_list]
        return TaskUserListSchema(items=items, limit=limit, offset=offset, total=total)
