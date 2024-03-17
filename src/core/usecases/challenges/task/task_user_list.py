from dataclasses import dataclass

from src.core.dto.utils import IterableObj
from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.exception.user import UserNotActive
from src.core.interfaces.repository.challenges.task import (
    SortUserTaskObj,
    TaskUserFilter,
)
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[TaskUser]
    limit: int | None
    offset: int
    total: int


class UserTaskListUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self,
        *,
        user: User,
        filter_obj: TaskUserFilter,
        sorting_obj: SortUserTaskObj,
        iterable_obj: IterableObj,
    ) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            lst = await uow.task.user_task_lst(
                user_id=user.id,
                filter_obj=filter_obj,
                sorting_obj=sorting_obj,
                iterable_obj=iterable_obj,
            )

        return Result(items=lst.items, limit=lst.limit, offset=lst.offset, total=lst.total)
