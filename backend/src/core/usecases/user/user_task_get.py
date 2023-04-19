from dataclasses import dataclass

from src.core.entity.task import TaskCreateDTO, TaskDTO
from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: TaskDTO


class TaskGetUseCase:
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User = None, obj: TaskCreateDTO) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)

        task = await self.repo.task_get(user_id=user.username, obj=obj)

        return Result(item=task)
