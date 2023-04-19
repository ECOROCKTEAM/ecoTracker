from dataclasses import dataclass

from src.core.dto.application_role import ApplicationRoleCreateDTO, ApplicationRoleDTO
from src.core.interfaces.base import IRepositoryCore
from src.core.exception.user import UserPermissionError
from src.core.entity.user import User


@dataclass
class Result:
    item: ApplicationRoleDTO


class TaskCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: ApplicationRoleCreateDTO) -> Result:

        #Как тогда создать первые роли? Возможно роли приложения надо будет создавать как-то при деплое что ли, я хз.
        
        if not user.application_role.ADMIN:
            raise UserPermissionError(username=user.username)

        app_role = await self.repo.user_role_application_create(obj=obj)

        return Result(item=app_role)
        