import asyncio
from dataclasses import dataclass
from src.core.dto.m2m.user.community import UserCommunityDTO

from src.core.entity.community import Community, CommunityUpdateDTO
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.dto.community.filters import CommunityIncludeUserFilter
from src.core.exception.community import CommunityDeactivatedError
from src.core.exception.user import (
    UserIsNotCommunityAdminUserError,
    UserIsNotPremiumError,
)
from src.core.interfaces.repository.community.community import IRepositoryCommunity


@dataclass
class Result:
    item: Community


class CommunityUpdateUsecase:
    def __init__(self, repo: IRepositoryCommunity) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, community_id: str, update_obj: CommunityUpdateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        tasks: tuple[asyncio.Task[Community], asyncio.Task[list[UserCommunityDTO]]] = (
            asyncio.create_task(self.repo.get(id=community_id)),
            asyncio.create_task(
                self.repo.user_list(
                    id=community_id,
                    filter=CommunityIncludeUserFilter(role_list=[CommunityRoleEnum.SUPERUSER, CommunityRoleEnum.ADMIN]),
                )
            ),
        )
        community, link_list = await asyncio.gather(*tasks)
        head_user_ids = [link.user_id for link in link_list]
        if user.username not in head_user_ids:
            raise UserIsNotCommunityAdminUserError(username=user.username, community_id=community_id)
        if not community.active:
            raise CommunityDeactivatedError(community_id=community.name)
        community = await self.repo.update(id=community_id, obj=update_obj)
        return Result(item=community)
