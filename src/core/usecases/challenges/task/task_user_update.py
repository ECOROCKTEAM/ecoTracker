from dataclasses import dataclass
from datetime import datetime

from src.core.dto.challenges.task import TaskUserPlanCreateDTO, TaskUserUpdateDTO
from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: TaskUser


class UserTaskUpdateUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, obj: TaskUserUpdateDTO) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        async with self.uow as uow:
            if obj.status == OccupancyStatusEnum.FINISH:
                user_task_id = await uow.task.user_task_get(user_id=user.id, task_id=obj.task_id)
                # Возможно тут проверка на то, что в UserTaskPlan уже есть такой таск, не нужна, если у нас update метод
                await uow.task.plan_create(obj=TaskUserPlanCreateDTO(user_id=user.id, task_id=user_task_id.task_id))

                # После мёрджа score репы и UC, добавить метод на добавление очков пользователю за выполненный таск

            today = datetime.today().replace(microsecond=0)
            updated_obj = await uow.task.user_task_update(
                obj=TaskUserUpdateDTO(
                    task_id=obj.task_id,
                    user_id=user.id,
                    date_close=today,
                    status=obj.status,
                ),
            )
            await uow.commit()
            return Result(item=updated_obj)
