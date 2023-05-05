import asyncio
from datetime import datetime, timedelta
import os
import binascii
from dataclasses import dataclass
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.community import (
    CommunityDeactivatedError,
    CommunityInviteLinkNotFoundError,
)

from src.core.exception.user import (
    UserIsNotCommunityAdminUserError,
    UserIsNotPremiumError,
)
from src.core.interfaces.repository.community.community import CommunityUserFilter, IRepositoryCommunity
from src.core.dto.community.invite import (
    CommunityInviteCreateDTO,
    CommunityInviteDTO,
    CommunityInviteUpdateDTO,
)
from src.core.entity.community import Community
import contextlib


@dataclass
class Result:
    item: CommunityInviteDTO


class CommunityGetInviteLinkUsecase:
    def __init__(self, *, repo: IRepositoryCommunity) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, community_id: str) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
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
        if not community.active:
            raise CommunityDeactivatedError(community_id=community.name)
        head_user_ids = [link.user_id for link in link_list]
        if user.username not in head_user_ids:
            raise UserIsNotCommunityAdminUserError(username=user.username, community_id=community_id)

        link = None
        with contextlib.suppress(CommunityInviteLinkNotFoundError):
            link = await self.repo.invite_link_get(id=community.name)

        random_hex = binascii.hexlify(os.urandom(16)).decode()
        next_time = datetime.now() + timedelta(weeks=1)
        expire_time = int(next_time.timestamp())

        if link is None:
            create_obj = CommunityInviteCreateDTO(community_id=community_id, code=random_hex, expire_time=expire_time)
            link = await self.repo.invite_link_create(obj=create_obj)
            return Result(item=link)

        update_obj = CommunityInviteUpdateDTO(community_id=community_id, code=random_hex, expire_time=expire_time)
        link = await self.repo.invite_link_update(obj=update_obj)
        return Result(item=link)
