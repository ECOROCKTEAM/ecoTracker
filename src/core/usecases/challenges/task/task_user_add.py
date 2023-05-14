from dataclasses import dataclass
from datetime import date

from src.core.dto.challenges.task import TaskUserCreateDTO
from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.user import TaskAlreadyTakenErro, UserIsNotActivateError, UserTaskMaxAmountError
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
            # Добавил в plan_lst\user_task_lst методы репоз None из-за того, что тут нам фильтры по сути не нужны
            user_tasks = await uow.task.user_task_lst()

            for obj in user_tasks:
                if task_id == obj.task_id:
                    raise TaskAlreadyTakenErro(user_id=user.id, task_id=task_id)

            finiched_user_tasks = [obj for obj in user_tasks if obj.status == OccupancyStatusEnum.FINISH]

            if not user.is_premium and len(finiched_user_tasks) > 3 and len(finiched_user_tasks) > 3:
                raise UserTaskMaxAmountError(user_id=user.id)

            if user.is_premium and len(finiched_user_tasks) > 10:
                raise UserTaskMaxAmountError(user_id=user.id)

            today = date.today()
            user_task_add = await uow.task.user_task_create(
                obj=TaskUserCreateDTO(date=today, user_id=user.id, task_id=task_id),
            )

            await uow.commit()

        return Result(item=user_task_add)
