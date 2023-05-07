from dataclasses import dataclass

from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.user import (
    UserIsNotPremiumError,
    UserIsNotCommunitySuperUserError,
)
from src.core.interfaces.repository.community.community import CommunityUserFilter, IRepositoryCommunity


@dataclass
class Result:
    item: int


class CommunityDeleteUsecase:
    def __init__(self, repo: IRepositoryCommunity) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, community_id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        link_list = await self.repo.user_list(
            id=community_id,
            filter_obj=CommunityUserFilter(role_list=[CommunityRoleEnum.SUPERUSER]),
        )
        super_user_ids = [link.user_id for link in link_list]
        if user.id not in super_user_ids:
            raise UserIsNotCommunitySuperUserError(user_id=user.id, community_id=community_id)
        deactivate_id = await self.repo.deactivate(id=community_id)
        return Result(item=deactivate_id)
