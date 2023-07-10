from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4

from src.core.dto.community.invite import CommunityInviteDTO, CommunityInviteUpdateDTO
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.base import EntityNotActive, PermissionError
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: CommunityInviteDTO


class CommunityGetInviteCodeUsecase:
    def __init__(self, *, uow: IUnitOfWork, invite_expire_sec: int) -> None:
        self.uow = uow
        self.invite_expire_sec = invite_expire_sec

    async def __call__(self, *, user: User, community_id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            community = await uow.community.get(id=community_id)
            if not community.active:
                raise EntityNotActive(msg=f"community_id={community.id}")
            community_user = await uow.community.user_get(community_id=community_id, user_id=user.id)
            if community_user.role not in (CommunityRoleEnum.ADMIN, CommunityRoleEnum.SUPERUSER):
                raise PermissionError(msg=f"user_id={user.id}, {community_id=}")
            invite = await uow.community.code_get(id=community_id)
            if invite.code is None or invite.expire_time is None or invite.expire_time < datetime.utcnow():
                obj = CommunityInviteUpdateDTO(
                    code=uuid4().hex, expire_time=datetime.utcnow() + timedelta(seconds=self.invite_expire_sec)
                )
                invite = await uow.community.code_set(id=community_id, obj=obj)
                await uow.commit()

            return Result(
                item=CommunityInviteDTO(
                    community_id=invite.community_id,
                    code=invite.code,
                    expire_time=invite.expire_time,
                )
            )
