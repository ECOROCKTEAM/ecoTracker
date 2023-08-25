from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4

from src.core.dto.group.invite import GroupInviteDTO, GroupInviteUpdateDTO
from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive, PermissionError
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: GroupInviteDTO


class GroupGetInviteCodeUsecase:
    def __init__(self, *, uow: IUnitOfWork, invite_expire_sec: int) -> None:
        self.uow = uow
        self.invite_expire_sec = invite_expire_sec

    async def __call__(self, *, user: User, group_id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            group = await uow.group.get(id=group_id)
            if not group.active:
                raise EntityNotActive(msg=f"group_id={group.id}")
            group_user = await uow.group.user_get(group_id=group_id, user_id=user.id)
            if group_user.role not in (GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER):
                raise PermissionError(msg=f"user_id={user.id}, {group_id=}")
            invite = await uow.group.code_get(id=group_id)
            if invite.code is None or invite.expire_time is None or invite.expire_time < datetime.utcnow():
                obj = GroupInviteUpdateDTO(
                    code=uuid4().hex, expire_time=datetime.utcnow() + timedelta(seconds=self.invite_expire_sec)
                )
                invite = await uow.group.code_set(id=group_id, obj=obj)
                await uow.commit()

            return Result(
                item=GroupInviteDTO(
                    group_id=invite.group_id,
                    code=invite.code,
                    expire_time=invite.expire_time,
                )
            )
