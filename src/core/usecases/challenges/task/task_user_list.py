from dataclasses import dataclass

from src.core.dto.mock import MockObj
from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.repository.challenges.task import TaskUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[TaskUser]


class UserTaskListUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self,
        *,
        user: User,
        filter_obj: TaskUserFilter,
        order_obj: MockObj,
        pagination_obj: MockObj,
    ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        async with self.uow as uow:
            lst = await uow.task.user_task_lst(
                filter_obj=filter_obj,
                order_obj=order_obj,
                pagination_obj=pagination_obj,
            )

        return Result(items=lst)
