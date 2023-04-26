from dataclasses import dataclass

from src.core.entity.task import TaskCreateDTO
from src.core.interfaces.task_repo.task import ITaskRepository
from src.core.entity.user import User
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item_id: int


class TaskDeleteUseCase:
    def __init__(self, repo: ITaskRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User = None, obj: TaskCreateDTO) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        # Захотим ли мы удалять какой-то таск (к миссиям тоже относится), если этот таск взят пользователем и находится в активном статусе?
        # Если да, то сделаю проверку. Если нет - оставлю как есть.

        task = await self.repo.delete(obj=obj)
        return Result(item=task)
