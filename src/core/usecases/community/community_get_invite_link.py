from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4

from src.core.dto.community.invite import CommunityInviteDTO, CommunityInviteUpdateDTO
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.community import CommunityDeactivatedError
from src.core.exception.user import (
    UserIsNotCommunityAdminUserError,
    UserIsNotPremiumError,
)
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: CommunityInviteDTO


class CommunityGetInviteLinkUsecase:
    def __init__(self, *, uow: IUnitOfWork, invite_expire_sec: int) -> None:
        self.uow = uow
        self.invite_expire_sec = invite_expire_sec

    async def __call__(self, *, user: User, community_id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            community = await uow.community.get(id=community_id)
            if not community.active:
                raise CommunityDeactivatedError(community_id=community.id)
            role = await uow.community.user_get(community_id=community_id, user_id=user.id)
            if role.role not in (CommunityRoleEnum.ADMIN, CommunityRoleEnum.SUPERUSER):
                raise UserIsNotCommunityAdminUserError(user_id=user.id, community_id=community_id)
            community_code = await uow.community.code_get(id=community_id)
            if not community_code.code:
                obj = CommunityInviteUpdateDTO(
                    code=uuid4().hex, expire_time=datetime.utcnow() + timedelta(seconds=self.invite_expire_sec)
                )
                community_code = await uow.community.code_set(id=community_id, obj=obj)
                await uow.commit()

            # create_link(community_code)
            return Result(item=community_code)
