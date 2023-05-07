import asyncio
from dataclasses import dataclass
from src.core.dto.m2m.user.community import UserCommunityDTO

from src.core.entity.community import Community
from src.core.dto.community.community import CommunityUpdateDTO
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.community import CommunityDeactivatedError
from src.core.exception.user import (
    UserIsNotCommunityAdminUserError,
    UserIsNotPremiumError,
)
from src.core.interfaces.repository.community.community import IRepositoryCommunity, CommunityUserFilter


@dataclass
class Result:
    item: Community


class CommunityUpdateUsecase:
    def __init__(self, repo: IRepositoryCommunity) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, community_id: int, update_obj: CommunityUpdateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        tasks: tuple[asyncio.Task[Community], asyncio.Task[list[UserCommunityDTO]]] = (
            asyncio.create_task(self.repo.get(id=community_id)),
            asyncio.create_task(
                self.repo.user_list(
                    id=community_id,
                    filter_obj=CommunityUserFilter(role_list=[CommunityRoleEnum.SUPERUSER, CommunityRoleEnum.ADMIN]),
                )
            ),
        )
        community, link_list = await asyncio.gather(*tasks)
        head_user_ids = [link.user_id for link in link_list]
        if user.id not in head_user_ids:
            raise UserIsNotCommunityAdminUserError(user_id=user.id, community_id=community_id)
        if not community.active:
            raise CommunityDeactivatedError(community_id=community.id)
        community = await self.repo.update(id=community_id, obj=update_obj)
        return Result(item=community)
