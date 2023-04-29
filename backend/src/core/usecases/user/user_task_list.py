from dataclasses import dataclass

from src.core.dto.m2m.user.filters import UserTaskFilter
from src.core.dto.mock import MockObj
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

    async def __call__(
        self, *,
        user: User,
        filter_obj: UserTaskFilter,
     ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)

        task_list = await self.repo.list(user_id=user.username, filter_obj=filter_obj)
        return Result(item=task_list)
