from dataclasses import dataclass

from src.core.dto.challenges.task import TaskUserUpdateDTO
from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotChange
from src.core.exception.user import UserNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: TaskUser


class UserTaskRejectUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            user_task = await uow.task.user_task_get(user_id=user.id, id=id)
            if not user_task.status == OccupancyStatusEnum.ACTIVE:
                raise EntityNotChange(msg=f"user_task.id={id}")

            # if not user.is_premium:
            #     """Проверка на удаление 3-x задач."""

            # if user.is_premium:
            #     """Проверка на удаление 10-ти задач."""

            task = await uow.task.user_task_update(
                user_id=user.id,
                id=id,
                obj=TaskUserUpdateDTO(status=OccupancyStatusEnum.REJECT),
            )

        return Result(item=task)
