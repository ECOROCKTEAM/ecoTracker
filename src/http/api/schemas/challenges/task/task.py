from fastapi import Query
from pydantic import BaseModel

from src.core.entity.task import Task
from src.core.enum.language import LanguageEnum
from src.core.interfaces.repository.challenges.task import TaskFilter


class TaskFilterSchema(BaseModel):
    active: bool | None = Query(default=None)
    category_id: int | None = Query(default=None)

    def to_obj(self) -> TaskFilter:
        return TaskFilter(active=self.active, category_id=self.category_id)


class TaskSchema(BaseModel):
    id: int
    score: int
    category_id: int
    name: str
    active: bool
    description: str
    language: LanguageEnum

    @classmethod
    def from_obj(cls, task: Task) -> "TaskSchema":
        return TaskSchema(
            id=task.id,
            score=task.score,
            category_id=task.category_id,
            name=task.name,
            active=task.active,
            description=task.description,
            language=task.language,
        )


class TaskListSchema(BaseModel):
    items: list[TaskSchema]
    limit: int | None
    offset: int
    total: int

    @classmethod
    def from_obj(cls, *, task_list: list[Task], limit: int | None, offset: int, total: int) -> "TaskListSchema":
        items = [
            TaskSchema(
                id=item.id,
                score=item.score,
                category_id=item.category_id,
                name=item.name,
                active=item.active,
                description=item.description,
                language=item.language,
            )
            for item in task_list
        ]
        return TaskListSchema(items=items, limit=limit, offset=offset, total=total)
