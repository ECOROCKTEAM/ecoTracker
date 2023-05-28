from dataclasses import dataclass
from datetime import datetime

from src.core.dto.challenges.task import TaskUserUpdateDTO
from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.user import UserIsNotActivateError, UserTaskStatusError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: TaskUser


class UserTaskCompleteUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, task_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        async with self.uow as uow:
            user_task = await uow.task.user_task_get(user_id=user.id, task_id=task_id)
            if not user_task.status.ACTIVE:
                raise UserTaskStatusError(task_id=task_id)

            if user.is_premium:
                """Проверка на 10 тасков в день"""

            if not user.is_premium:
                """Проверка на 3 таска в день"""

            """ Добавить после мержа метод на добавление очков за завершённый таск """

            result = await uow.task.user_task_update(
                user_id=user.id,
                task_id=task_id,
                obj=TaskUserUpdateDTO(status=OccupancyStatusEnum.FINISH, date_close=datetime.now()),
            )
            """ Добавлять ли тут ещё и date_close, когда пользователь ВЫПОЛНЯЕТ таск? """

        return Result(item=result)
