from dataclasses import dataclass

from src.core.entity.task import Task
from src.core.interfaces.repository.challenges.task import IRepositoryTask
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: Task


class TaskGetUseCase:
    def __init__(self, repo: IRepositoryTask) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, task_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        task = await self.repo.get(id=task_id, lang=user.language)

        return Result(item=task)
