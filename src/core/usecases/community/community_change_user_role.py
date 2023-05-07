import asyncio
from dataclasses import dataclass

from src.core.dto.m2m.user.community import UserCommunityUpdateDTO, UserCommunityDTO
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.community import (
    CommunityDeactivatedError,
)
from src.core.exception.user import (
    UserIsNotCommunityAdminUserError,
    UserIsNotPremiumError,
    UserIsNotCommunitySuperUserError,
)
from src.core.interfaces.repository.community.community import IRepositoryCommunity, CommunityUserFilter


@dataclass
class Result:
    item: UserCommunityDTO


class CommunityChangeUserRoleUsecase:
    def __init__(self, *, repo: IRepositoryCommunity) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, update_obj: UserCommunityUpdateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        community_id = update_obj.community_id
        tasks: tuple[asyncio.Task[Community], asyncio.Task[list[UserCommunityDTO]]] = (
            asyncio.create_task(self.repo.get(id=community_id)),
            asyncio.create_task(
                self.repo.user_list(
                    id=community_id,
                    filter_obj=CommunityUserFilter(role_list=[CommunityRoleEnum.SUPERUSER, CommunityRoleEnum.ADMIN]),
                )
            ),
        )
        (
            community,
            link_list_head_user,
        ) = await asyncio.gather(*tasks)
        if not community.active:
            raise CommunityDeactivatedError(community_id=community.id)

        current_user_link = None
        target_user_link = None
        for _link in link_list_head_user:
            if user.id == _link.user_id:
                current_user_link = _link
            if update_obj.user_id == _link.user_id:
                target_user_link = _link
        # User role must be ADMIN or SUPERUSER
        if current_user_link is None:
            raise UserIsNotCommunityAdminUserError(user_id=user.id, community_id=community_id)

        # ADMIN can't change role for SUPERUSER
        if target_user_link and target_user_link.role.SUPERUSER and current_user_link.role.ADMIN:
            raise UserIsNotCommunitySuperUserError(
                user_id=current_user_link.user_id,
                community_id=current_user_link.community_id,
            )

        link = await self.repo.user_role_update(obj=update_obj)
        return Result(item=link)
