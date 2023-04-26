from dataclasses import dataclass

from src.core.dto.m2m.user.task import UserTaskDTO
from src.core.interfaces.user.task import IUserTaskRepository
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: list[UserTaskDTO]


class UserTaskListUseCase:
    def __init__(self, repo: IUserTaskRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)

        task = await self.repo.list(user_id=user.username)
        return Result(item=task)
