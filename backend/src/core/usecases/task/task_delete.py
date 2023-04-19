from dataclasses import dataclass

from src.core.dto.tasks import TaskCreateDTO
from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item_id: int


class TaskDeleteUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User = None, obj: TaskCreateDTO) -> Result:
        
        if not user.application_role.ADMIN:
            raise UserPermissionError(username=user.username)

        task = await self.repo.task_delete(obj=obj)

        return Result(item=task)
        