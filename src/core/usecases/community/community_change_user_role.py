from dataclasses import dataclass

from src.core.dto.m2m.user.community import UserCommunityUpdateDTO, UserCommunityDTO
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

from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: UserCommunityDTO


class CommunityChangeUserRoleUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self, *, user: User, community_id: int, user_id: int, update_obj: UserCommunityUpdateDTO
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            community = await uow.community.get(id=community_id)

            if not community.active:
                raise CommunityDeactivatedError(community_id=community.id)
            current_user = await uow.community.user_get(user_id=user.id, community_id=community_id)
            if current_user.role not in (CommunityRoleEnum.SUPERUSER, CommunityRoleEnum.ADMIN):
                raise UserIsNotCommunityAdminUserError(user_id=user.id, community_id=community_id)

            target_user = await uow.community.user_get(community_id=community_id, user_id=user_id)
            if target_user.role == CommunityRoleEnum.SUPERUSER and current_user.role != CommunityRoleEnum.SUPERUSER:
                raise UserIsNotCommunitySuperUserError(
                    username=user_id,
                    community_id=community_id,
                )
            link = await uow.community.user_role_update(obj=update_obj, community_id=community_id, user_id=user_id)
            await uow.commit()
        return Result(item=link)
