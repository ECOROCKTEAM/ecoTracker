from dataclasses import dataclass

from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    task_id: int


# Fix after rebuild tasks architecture


class UserTaskDeleteUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, task_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        # Подумать на работе над ограничениями при удалении тасков обычному пользователю

        async with self.uow as uow:
            if not user.is_premium:
                """
                Если у нас будет редис, может там хранить ключ с userid_task_deleted и значением int,
                которое будет увеличиваться на +=1, когда обычный пользователь будет удалять у себя таск?

                Если так, то тут будет get в redis и проверка значения.
                """

            if user.is_premium:
                """Проверка на удаление 10-ти задач."""

            task_id = await uow.task.user_task_delete(
                user_id=user.id,
                task_id=task_id,
            )

        return Result(task_id=task_id)
