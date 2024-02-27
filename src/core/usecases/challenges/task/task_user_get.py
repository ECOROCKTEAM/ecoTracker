from dataclasses import dataclass

from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.exception.user import UserNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: TaskUser


class UserTaskGetUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            user_task = await uow.task.user_task_get(user_id=user.id, id=id)

        return Result(item=user_task)
