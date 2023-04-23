from dataclasses import dataclass

from src.core.dto.user.role import UserRoleCreateDTO, UserRoleDTO
from src.core.interfaces.user.application_role import IApplicationRoleRepository
from src.core.exception.user import UserPermissionError
from src.core.entity.user import User


@dataclass
class Result:
    item: UserRoleDTO


class TaskCreateUseCase:
    def __init__(self, repo: IApplicationRoleRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: UserRoleCreateDTO) -> Result:

        if not user.application_role.ADMIN:
            raise UserPermissionError(username=user.username)

        app_role = await self.repo.application_create(obj=obj)

        return Result(item=app_role)
