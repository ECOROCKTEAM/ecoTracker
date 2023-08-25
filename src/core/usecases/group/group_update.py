from dataclasses import dataclass

from src.core.dto.group.group import GroupUpdateDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive, PermissionError
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: Group


class GroupUpdateUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, group_id: int, update_obj: GroupUpdateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            group = await uow.group.get(id=group_id)
            if not group.active:
                raise EntityNotActive(msg=f"{group.id}")
            user_role = await uow.group.user_get(group_id=group_id, user_id=user.id)
            if user_role.role not in (GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER):
                raise PermissionError(msg=f"{user.id=}, {group_id=}")
            group = await uow.group.update(id=group_id, obj=update_obj)
            await uow.commit()
        return Result(item=group)
