import asyncio
from dataclasses import dataclass
from src.core.dto.community_role import CommunityRoleCreateDTO, CommunityRoleDTO

from src.core.exception.user import UserPermissionError
from src.core.interfaces.repository.core import IRepositoryCore


@dataclass
class Result:
    item: CommunityRoleDTO


class CommunityRoleCreateUsecase:
    def __init__(self, *, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user_id: str, create_obj: CommunityRoleCreateDTO) -> Result:
        user_task = asyncio.create_task(self.repo.user_get(id=user_id))
        user = await user_task
        if not user.application_role.ADMIN:
            raise UserPermissionError(user_id=user_id)
        role = await self.repo.community_role_create(obj=create_obj)
        return Result(item=role)
