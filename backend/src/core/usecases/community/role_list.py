from dataclasses import dataclass
from src.core.dto.community.role import CommunityRoleDTO
from src.core.entity.user import User

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.core import IRepositoryCore


@dataclass
class Result:
    item: list[CommunityRoleDTO]


class CommunityRoleCreateUsecase:
    def __init__(self, *, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        privacy_list = await self.repo.community_role_list()
        return Result(item=privacy_list)
