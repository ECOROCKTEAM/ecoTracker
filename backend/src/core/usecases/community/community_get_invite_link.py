import asyncio
from datetime import datetime, timedelta
import os
import binascii
from dataclasses import dataclass
from typing import Tuple
from src.core.dto.shared import UserCommunityDTO
from src.core.entity.user import User
from src.core.enum.role import CommunityRoleEnum
from src.core.exception.community import (
    CommunityDeactivatedError,
    CommunityInviteLinkNotFoundError,
)

from src.core.exception.user import (
    UserIsNotCommunityAdminUserError,
    UserIsNotPremiumError,
)
from src.core.interfaces.repository.core import IRepositoryCore
from src.core.dto.community import (
    CommunityIncludeUserFilter,
    CommunityInviteCreateDTO,
    CommunityInviteDTO,
    CommunityInviteUpdateDTO,
)
from src.core.entity.community import Community


@dataclass
class Result:
    item: CommunityInviteDTO


class CommunityGetInviteLinkUsecase:
    def __init__(self, *, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, community_id: str) -> Result:
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
        if not community.active:
            raise CommunityDeactivatedError(community_id=community.name)
        head_user_ids = [l.user_id for l in link_list]
        if not user.username in head_user_ids:
            raise UserIsNotCommunityAdminUserError(
                username=user.username, community_id=community_id
            )

        link = None
        try:
            link = await self.repo.community_invite_link_get(
                community_id=community.name
            )
        except CommunityInviteLinkNotFoundError:
            pass

        random_hex = binascii.hexlify(os.urandom(16)).decode()
        next_time = datetime.now() + timedelta(weeks=1)
        expire_time = int(next_time.timestamp())

        if link is None:
            create_obj = CommunityInviteCreateDTO(
                community_id=community_id, code=random_hex, expire_time=expire_time
            )
            link = await self.repo.community_invite_link_create(obj=create_obj)
            return Result(item=link)

        update_obj = CommunityInviteUpdateDTO(
            community_id=community_id, code=random_hex, expire_time=expire_time
        )
        link = await self.repo.community_invite_link_update(obj=update_obj)
        return Result(item=link)
