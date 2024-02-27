from dataclasses import dataclass

from src.core.const.task import MAX_TASK_AMOUNT_NOT_PREMIUM, MAX_TASK_AMOUNT_PREMIUM
from src.core.dto.challenges.task import TaskUserCreateDTO
from src.core.dto.utils import IterableObj, SortObj
from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityAlreadyUsage, EntityNotActive, MaxAmountError
from src.core.exception.user import UserNotActive
from src.core.interfaces.repository.challenges.task import (
    TaskUserFilter,
    TaskUserPlanFilter,
)
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: TaskUser


class UserTaskAddUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, task_id: int) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            task = await uow.task.get(id=task_id, lang=user.language)
            if not task.active:
                raise EntityNotActive(msg=f"task.id={task_id}")

            max_count = MAX_TASK_AMOUNT_NOT_PREMIUM
            if user.is_premium:
                max_count = MAX_TASK_AMOUNT_PREMIUM

            user_tasks_pagination = await uow.task.user_task_lst(
                user_id=user.id,
                filter_obj=TaskUserFilter(status=OccupancyStatusEnum.ACTIVE),
                sorting_obj=SortObj(),
                iterable_obj=IterableObj(),
            )
            user_tasks = user_tasks_pagination.items

            for user_task in user_tasks:
                if user_task.task_id == task_id:
                    raise EntityAlreadyUsage(msg=f"{user.id=}, task.id={task_id}")

            if len(user_tasks) > max_count:
                raise MaxAmountError(msg=f"{user.id=}")

            user_plan_tasks_pagination = await uow.task.plan_lst(
                user_id=user.id, filter_obj=TaskUserPlanFilter(), sorting_obj=SortObj(), iterable_obj=IterableObj()
            )
            user_plan_tasks = user_plan_tasks_pagination.items

            if len(user_plan_tasks) > max_count:
                raise MaxAmountError(msg=f"{user.id=}")

            user_task_add = await uow.task.user_task_add(
                user_id=user.id,
                obj=TaskUserCreateDTO(task_id=task_id, status=OccupancyStatusEnum.ACTIVE),
            )

            await uow.commit()

        return Result(item=user_task_add)
