from dataclasses import dataclass

from src.core.dto.utils import IterableObj, SortObj
from src.core.entity.task import TaskUserPlan
from src.core.entity.user import User
from src.core.exception.user import UserNotActive
from src.core.interfaces.repository.challenges.task import TaskUserPlanFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[TaskUserPlan]
    limit: int | None
    offset: int
    total: int


class UserTaskPlanListUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self,
        *,
        user: User,
        filter_obj: TaskUserPlanFilter,
        sorting_obj: SortObj,
        iterable_obj: IterableObj,
    ) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            plan_list = await uow.task.plan_lst(
                user_id=user.id,
                filter_obj=filter_obj,
                sorting_obj=sorting_obj,
                iterable_obj=iterable_obj,
            )

        return Result(items=plan_list.items, limit=plan_list.limit, offset=plan_list.offset, total=plan_list.total)
