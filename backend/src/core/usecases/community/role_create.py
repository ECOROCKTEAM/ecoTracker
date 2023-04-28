from dataclasses import dataclass
from src.core.dto.community.role import CommunityRoleCreateDTO, CommunityRoleDTO
from src.core.entity.user import User

from src.core.exception.user import UserPermissionError
from src.core.interfaces.repository.core import IRepositoryCore


@dataclass
class Result:
    item: CommunityRoleDTO


class CommunityRoleCreateUsecase:
    def __init__(self, *, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(
        self, *, user: User, create_obj: CommunityRoleCreateDTO
    ) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)
        role = await self.repo.community_role_create(obj=create_obj)
        return Result(item=role)
