from dataclasses import dataclass, field

from src.core.exception.user import UserIsNotActivateError
from src.core.entity.task import Task
from src.core.entity.user import User
from src.core.dto.mock import MockObj
from src.core.interfaces.repository.challenges.task import TaskFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[Task] = field(default_factory=list)


class TaskListUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self,
        *,
        user: User,
        sorting_obj: MockObj,
        paggination_obj: MockObj,
        filter_obj: TaskFilter,
    ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        filter_obj.active = True

        async with self.uow as uow:
            task_list = await uow.task.lst(
                sorting_obj=sorting_obj,
                pagination_obj=paggination_obj,
                filter_obj=filter_obj,
                lang=user.language,
            )
        return Result(items=task_list)
