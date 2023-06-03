from dataclasses import dataclass

from src.core.entity.task import Task
from src.core.entity.user import User
from src.core.exception.task import TaskDeactivatedError
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: Task


class TaskGetUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, task_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        async with self.uow as uow:
            task = await uow.task.get(id=task_id, lang=user.language)
            if not task.active:
                raise TaskDeactivatedError(task_id=task.id)
        return Result(item=task)
