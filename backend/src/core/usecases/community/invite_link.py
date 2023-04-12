import asyncio
from dataclasses import dataclass
from typing import Tuple
from src.core.entity.user import User
from src.core.enum.role import CommunityRoleEnum

from src.core.exception.user import UserIsNotCommunityAdminUserError, UserIsNotPremiumError
from src.core.interfaces.repository.core import IRepositoryCore
from src.core.dto.community import CommunityIncludeUserFilter
from src.core.entity.community import Community


@dataclass
class Result:
    item: list[Community]


class CommunityInviteLinkUsecase:
    def __init__(self, *, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user_id: str, community_id: str) -> Result:
        tasks: Tuple[asyncio.Task[User], asyncio.Task[list[str]]] = (
            asyncio.create_task(self.repo.user_get(id=user_id)),
            asyncio.create_task(
                self.repo.community_user_ids(
                    id=community_id,
                    filter=CommunityIncludeUserFilter(role_list=[CommunityRoleEnum.SUPERUSER, CommunityRoleEnum.ADMIN]),
                )
            ),
        )
        user, head_user_ids = await asyncio.gather(*tasks)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user_id)
        if not user.id in head_user_ids:
            raise UserIsNotCommunityAdminUserError(user_id=user_id, community_id=community_id)
        # community_list = await self.repo.community_list(obj=filter_obj)
        # return Result(item=community_list)
