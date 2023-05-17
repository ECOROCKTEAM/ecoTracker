from dataclasses import dataclass
from datetime import datetime

from src.core.dto.challenges.task import TaskUserUpdateDTO
from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.user import (
    UserCanNotRejectFinishedTaskError,
    UserDoesNotHaveThisTaskError,
    UserIsNotActivateError,
)
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: TaskUser


class UserTaskUpdateUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, task_id: int, obj: TaskUserUpdateDTO) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        async with self.uow as uow:
            task_user = await uow.task.user_task_get(user_id=user.id, task_id=task_id)

            if not task_user:
                raise UserDoesNotHaveThisTaskError(user_id=user.id, task_id=task_id)

            if obj.status == OccupancyStatusEnum.FINISH:
                # После мёрджа score репы и UC, добавить метод на добавление очков пользователю за выполненный таск
                """"""

            if obj.status == OccupancyStatusEnum.REJECT and task_user.status.FINISH:
                raise UserCanNotRejectFinishedTaskError(task_id=task_id)

            today = datetime.today().replace(microsecond=0)
            updated_obj = await uow.task.user_task_update(
                user_id=user.id,
                task_id=task_id,
                obj=TaskUserUpdateDTO(
                    date_close=today,
                    status=obj.status,
                ),
            )
            await uow.commit()
            return Result(item=updated_obj)
