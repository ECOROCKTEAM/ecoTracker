from dataclasses import dataclass

from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    task_id: int


class UserTaskDeleteUseCase:
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, task_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)

        add = await self.repo.user_task_delete(user_id=user.username, task_id=task_id)

        return Result(task_id=add)
