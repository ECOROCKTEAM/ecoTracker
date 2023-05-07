from dataclasses import dataclass, field

from src.core.interfaces.repository.challenges.task import IRepositoryTask
from src.core.exception.user import UserIsNotActivateError
from src.core.entity.task import Task
from src.core.entity.user import User
from src.core.dto.mock import MockObj


@dataclass
class Result:
    items: list[Task] = field(default_factory=list)


class TaskListUseCase:
    def __init__(self, repo: IRepositoryTask) -> None:
        self.repo = repo

    async def __call__(
        self,
        *,
        user: User,
        sorting_obj: MockObj,
        paggination_obj: MockObj,
        filter_obj: MockObj,
    ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        task_list = await self.repo.lst(
            sorting_obj=sorting_obj,
            paggination_obj=paggination_obj,
            filter_obj=filter_obj,
            return_language=user.language,
        )

        return Result(items=task_list)
