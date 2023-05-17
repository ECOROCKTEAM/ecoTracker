from dataclasses import dataclass
from datetime import date

from src.core.dto.challenges.task import TaskUserCreateDTO
from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.user import (
    TaskAlreadyTakenError,
    UserIsNotActivateError,
    UserTaskMaxAmountError,
)
from src.core.interfaces.repository.challenges.task import TaskUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: TaskUser


class UserTaskAddUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, task_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        async with self.uow as uow:
            filter_obj = TaskUserFilter(status=OccupancyStatusEnum.ACTIVE)

            user_tasks = await uow.task.user_task_lst(user_id=user.id, filter_obj=filter_obj)
            user_plan_tasks = await uow.task.plan_lst(user_id=user.id)

            if user_plan_tasks and user_tasks:
                for obj in user_tasks:
                    if task_id == obj.task_id:
                        raise TaskAlreadyTakenError(user_id=user.id, task_id=task_id)

                if not user.is_premium and (len(user_tasks) >= 3 or len(user_plan_tasks) >= 3):
                    raise UserTaskMaxAmountError(user_id=user.id)

                if user.is_premium and (len(user_tasks) >= 10 or len(user_plan_tasks) >= 10):
                    raise UserTaskMaxAmountError(user_id=user.id)

            today = date.today()
            user_task_add = await uow.task.user_task_create(
                user_id=user.id,
                obj=TaskUserCreateDTO(date_start=today, task_id=task_id),
            )

            await uow.commit()

        return Result(item=user_task_add)
