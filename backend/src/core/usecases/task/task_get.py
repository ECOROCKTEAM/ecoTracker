from dataclasses import dataclass

from src.core.entity.task import Task
from src.core.interfaces.task_repo.task import ITaskRepository
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: Task


class TaskGetUseCase:
    def __init__(self, repo: ITaskRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, task_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)

        task = await self.repo.get(obj=task_id)

        return Result(item=task)
