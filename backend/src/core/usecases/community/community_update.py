import asyncio
from typing import Tuple
from dataclasses import dataclass
from src.core.dto.shared import UserCommunityDTO

from src.core.entity.community import Community, CommunityUpdateDTO
from src.core.entity.user import User
from src.core.enum.role import CommunityRoleEnum
from src.core.dto.community import CommunityIncludeUserFilter
from src.core.exception.community import CommunityDeactivatedError
from src.core.exception.user import (
    UserIsNotCommunityAdminUserError,
    UserIsNotPremiumError,
)
from src.core.interfaces.repository.core import IRepositoryCore


@dataclass
class Result:
    item: Community


class CommunityUpdateUsecase:
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(
        self, *, user: User, community_id: str, update_obj: CommunityUpdateDTO
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        tasks: Tuple[asyncio.Task[Community], asyncio.Task[list[UserCommunityDTO]]] = (
            asyncio.create_task(self.repo.community_get(id=community_id)),
            asyncio.create_task(
                self.repo.community_user_list(
                    id=community_id,
                    filter=CommunityIncludeUserFilter(
                        role_list=[CommunityRoleEnum.SUPERUSER, CommunityRoleEnum.ADMIN]
                    ),
                )
            ),
        )
        community, link_list = await asyncio.gather(*tasks)
        head_user_ids = [l.user_id for l in link_list]
        if not user.username in head_user_ids:
            raise UserIsNotCommunityAdminUserError(
                username=user.username, community_id=community_id
            )
        if not community.active:
            raise CommunityDeactivatedError(community_id=community.name)
        community = await self.repo.community_update(id=community_id, obj=update_obj)
        return Result(item=community)
