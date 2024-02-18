from dataclasses import dataclass

from src.core.dto.statistic.user import TaskUserCounterDTO
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: TaskUserCounterDTO


class UserTasksFinishedCounterUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User) -> Result:
        if not user.active:
            raise EntityNotActive(msg=f"{user.id=}")

        async with self.uow as uow:
            task_counter = await uow.user_statistic.task_counter(user_id=user.id)

        return Result(item=task_counter)
