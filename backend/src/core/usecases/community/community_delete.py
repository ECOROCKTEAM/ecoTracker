from dataclasses import dataclass

from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.dto.community.filters import CommunityIncludeUserFilter
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
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        link_list = await self.repo.community_user_list(
            id=community_id,
            filter=CommunityIncludeUserFilter(role_list=[CommunityRoleEnum.SUPERUSER]),
        )
        super_user_ids = [l.user_id for l in link_list]
        if not user.username in super_user_ids:
            raise UserIsNotCommunitySuperUserError(
                username=user.username, community_id=community_id
            )
        deactivate_id = await self.repo.community_deactivate(id=community_id)
        return Result(item=deactivate_id)
