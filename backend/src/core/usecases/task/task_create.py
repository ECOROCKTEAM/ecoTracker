from dataclasses import dataclass

from src.core.dto.tasks import TaskCreateDTO, TaskDTO
from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: TaskDTO


class TaskCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: TaskCreateDTO) -> Result:

        if not user.application_role.ADMIN:
            raise UserPermissionError(username=user.username)
        
        task = await self.repo.task_create(obj=obj)


        return Result(item=task)
        