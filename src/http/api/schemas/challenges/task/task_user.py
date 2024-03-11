from datetime import datetime

from fastapi import Query
from pydantic import BaseModel

from src.core.entity.task import TaskUser
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.interfaces.repository.challenges.task import TaskUserFilter


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
    date_start: datetime
    date_close: datetime | None

    @classmethod
    def from_obj(cls, task_user: TaskUser) -> "TaskUserSchema":
        return TaskUserSchema(
            id=task_user.id,
            user_id=task_user.user_id,
            task_id=task_user.task_id,
            status=task_user.status,
            date_start=task_user.date_start,
            date_close=task_user.date_close,
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
        items = [
            TaskUserSchema(
                id=item.id,
                user_id=item.user_id,
                task_id=item.task_id,
                status=item.status,
                date_start=item.date_start,
                date_close=item.date_close,
            )
            for item in task_user_list
        ]
        return TaskUserListSchema(items=items, limit=limit, offset=offset, total=total)
