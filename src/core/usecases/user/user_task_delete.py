from dataclasses import dataclass

from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.repository.user.task import IUserTaskRepository


@dataclass
class Result:
    task_id: int


# Fix after rebuild tasks architecture


class UserTaskDeleteUseCase:
    def __init__(self, repo: IUserTaskRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        # Подумать на работе над ограничениями при удалении тасков обычному пользователю

        add = await self.repo.delete(id=obj_id)
        return Result(task_id=add)
