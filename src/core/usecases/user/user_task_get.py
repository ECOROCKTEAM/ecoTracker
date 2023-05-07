from dataclasses import dataclass

from src.core.dto.m2m.user.task import UserTaskDTO
from src.core.interfaces.repository.user.task import IUserTaskRepository
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: UserTaskDTO


class UserTaskGetUseCase:
    def __init__(self, repo: IUserTaskRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        task = await self.repo.get(id=obj_id)
        return Result(item=task)
