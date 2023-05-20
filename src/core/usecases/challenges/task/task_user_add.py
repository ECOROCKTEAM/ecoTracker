from dataclasses import dataclass
from datetime import date

from src.core.dto.challenges.task import TaskUserCreateDTO
from src.core.dto.mock import MockObj
from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.user import (
    TaskAlreadyTakenError,
    UserIsNotActivateError,
    UserTaskMaxAmountError,
)
from src.core.interfaces.repository.challenges.task import (
    TaskUserFilter,
    TaskUserPlanFilter,
)
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
            """
            Не костыль ли это?
            Вроде типо хардкод. Но будем ли мы получать order+pagination объекты,
            когда пользователь захочет просто себе добавить таск?
            """
            user_tasks = await uow.task.user_task_lst(
                user_id=user.id,
                filter_obj=TaskUserFilter(task_id=task_id, status=OccupancyStatusEnum.ACTIVE),
                pagination_obj=MockObj(),
                order_obj=MockObj(),
            )
            user_plan_tasks = await uow.task.plan_lst(
                user_id=user.id,
                filter_obj=TaskUserPlanFilter(),
                order_obj=MockObj(),
                pagination_obj=MockObj(),
            )

            if user_tasks:
                raise TaskAlreadyTakenError(user_id=user.id, task_id=task_id)

            max_count = 3
            if user.is_premium:
                max_count = 10

            if len(user_tasks) == max_count and len(user_plan_tasks) == max_count:
                raise UserTaskMaxAmountError(user_id=user.id)

            today = date.today()
            user_task_add = await uow.task.user_task_create(
                user_id=user.id,
                obj=TaskUserCreateDTO(date_start=today, task_id=task_id),
            )

            await uow.commit()

        return Result(item=user_task_add)
