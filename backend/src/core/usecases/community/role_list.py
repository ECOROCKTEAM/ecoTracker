import asyncio
from dataclasses import dataclass
from src.core.dto.community_role import CommunityRoleDTO

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.core import IRepositoryCore


@dataclass
class Result:
    item: list[CommunityRoleDTO]


class CommunityRoleCreateUsecase:
    def __init__(self, *, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user_id: str) -> Result:
        user = await self.repo.user_get(id=user_id)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user_id)
        privacy_list = await self.repo.community_role_list()
        return Result(item=privacy_list)
