from dataclasses import dataclass

from src.core.dto.utils import IterableObj, SortObj
from src.core.entity.task import Task
from src.core.entity.user import User
from src.core.exception.user import UserNotActive
from src.core.interfaces.repository.challenges.task import TaskFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[Task]
    limit: int | None
    offset: int
    total: int


class TaskListUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self,
        *,
        user: User,
        filter_obj: TaskFilter,
        sorting_obj: SortObj,
        iterable_obj: IterableObj,
    ) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        filter_obj.active = True

        async with self.uow as uow:
            task_list = await uow.task.lst(
                filter_obj=filter_obj,
                sorting_obj=sorting_obj,
                iterable_obj=iterable_obj,
                lang=user.language,
            )
        return Result(items=task_list.items, limit=task_list.limit, offset=task_list.offset, total=task_list.total)
