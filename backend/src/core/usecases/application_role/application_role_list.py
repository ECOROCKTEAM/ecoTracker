from dataclasses import dataclass

from src.core.dto.user.role import UserRoleDTO
from src.core.interfaces.repository.user.application_role import IApplicationRoleRepository
from src.core.exception.user import UserPermissionError
from src.core.entity.user import User


@dataclass
class Result:
    items: list[UserRoleDTO]


class ApplicationRoleListUseCase:
    def __init__(self, repo: IApplicationRoleRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        app_role_list = await self.repo.list()
        return Result(items=app_role_list)
