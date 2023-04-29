from dataclasses import dataclass

from src.core.interfaces.repository.user.task import IUserTaskRepository
from src.core.entity.user import User
from src.core.dto.m2m.user.task import UserTaskDTO, UserTaskUpdateDTO
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: UserTaskDTO


class UserTaskUpdateUseCase:
    def __init__(self, repo: IUserTaskRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: UserTaskUpdateDTO) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)

        add = await self.repo.update(obj=obj)
        return Result(item=add)
