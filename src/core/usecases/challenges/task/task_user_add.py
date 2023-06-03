from dataclasses import dataclass
from datetime import date

from src.core.dto.challenges.task import TaskUserCreateDTO
from src.core.dto.mock import MockObj
from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.task import TaskDeactivatedError
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
            task = await uow.task.get(id=task_id, lang=user.language)
            if not task.active:
                raise TaskDeactivatedError(task_id=task_id)

            """ 
            Всё-таки придётся добавить в фильтр task_id потому, что иначе мы никак не сможем получить
            нашу взятую/не взятую таскую. 
            """

            task_exist = await uow.task.user_task_lst(
                user_id=user.id,
                filter_obj=TaskUserFilter(task_id=task_id, status=OccupancyStatusEnum.ACTIVE),
                order_obj=MockObj(),
                pagination_obj=MockObj(),
            )

            if task_exist:
                raise TaskAlreadyTakenError(user_id=user.id, task_id=task_id)

            max_count = 3
            if user.is_premium:
                max_count = 10

            user_tasks = await uow.task.user_task_lst(
                user_id=user.id,
                filter_obj=TaskUserFilter(status=OccupancyStatusEnum.ACTIVE),
                pagination_obj=MockObj(),
                order_obj=MockObj(),
            )

            if len(user_tasks) == max_count:
                raise UserTaskMaxAmountError(user_id=user.id)

            user_plan_tasks = await uow.task.plan_lst(
                user_id=user.id,
                filter_obj=TaskUserPlanFilter(),
                order_obj=MockObj(),
                pagination_obj=MockObj(),
            )

            if len(user_plan_tasks) == max_count:
                raise UserTaskMaxAmountError(user_id=user.id)

            today = date.today()
            user_task_add = await uow.task.user_task_add(
                user_id=user.id,
                obj=TaskUserCreateDTO(date_start=today, task_id=task_id, status=OccupancyStatusEnum.ACTIVE),
            )

            await uow.commit()

        return Result(item=user_task_add)
