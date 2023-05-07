from dataclasses import dataclass

from src.core.dto.m2m.user.filters import UserTaskFilter
from src.core.dto.m2m.user.task import UserTaskDTO
from src.core.interfaces.repository.user.task import IUserTaskRepository
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: list[UserTaskDTO]


class UserTaskListUseCase:
    def __init__(self, repo: IUserTaskRepository) -> None:
        self.repo = repo

    async def __call__(
        self,
        *,
        user: User,
        filter_obj: UserTaskFilter,
    ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        task_list = await self.repo.list(user_id=user.id, filter_obj=filter_obj)
        return Result(item=task_list)
