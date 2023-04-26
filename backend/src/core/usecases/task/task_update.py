from dataclasses import dataclass

from src.core.entity.task import Task, TaskUpdateDTO
from src.core.interfaces.task_repo.task import ITaskRepository
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError, UserPermissionError


@dataclass
class Result:
    item: Task


class TaskUpdateUseCase:
    def __init__(self, repo: ITaskRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: TaskUpdateDTO) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)
        
        # Думаю, что ничего страшного, если мы изменим таск или миссию, будучи взятой какими-то пользователями

        task = await self.repo.update(obj=obj)
        return Result(item=task)
