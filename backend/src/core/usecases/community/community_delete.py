from dataclasses import dataclass

from src.core.entity.user import User
from src.core.enum.role import CommunityRoleEnum
from src.core.dto.community import CommunityIncludeUserFilter
from src.core.exception.user import (
    UserIsNotPremiumError,
    UserIsNotCommunitySuperUserError,
)
from src.core.interfaces.repository.core import IRepositoryCore


@dataclass
class Result:
    item: str


class CommunityDeleteUsecase:
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, community_id: str) -> Result:
        super_user_ids = await self.repo.community_user_ids(
            id=community_id,
            filter=CommunityIncludeUserFilter(role_list=[CommunityRoleEnum.SUPERUSER]),
        )
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        if not user.username in super_user_ids:
            raise UserIsNotCommunitySuperUserError(
                username=user.username, community_id=community_id
            )
        deactivate_id = await self.repo.community_deactivate(id=community_id)
        return Result(item=deactivate_id)
