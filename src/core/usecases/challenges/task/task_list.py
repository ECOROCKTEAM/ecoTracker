from dataclasses import dataclass, field

from src.core.interfaces.repository.challenges.task import ITaskRepository
from src.core.exception.user import UserIsNotActivateError
from src.core.entity.task import Task
from src.core.entity.user import User


@dataclass
class Result:
    items: list[Task] = field(default_factory=list)


class TaskListUseCase:
    def __init__(self, repo: ITaskRepository) -> None:
        self.repo = repo

    async def __call__(
        self,
        *,
        user: User,
        sorting_obj: str = None,
        paggination_obj: str = None,
        filter_obj: str = None,
    ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)

        task_list = await self.repo.list(
            sorting_obj=sorting_obj,
            paggination_obj=paggination_obj,
            filter_obj=filter_obj,
        )

        return Result(items=task_list)
