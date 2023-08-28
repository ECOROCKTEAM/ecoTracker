from dataclasses import dataclass

from src.core.dto.group.group import GroupCreateDTO
from src.core.dto.m2m.user.group import UserGroupCreateDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: Group


class GroupCreateUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, create_obj: GroupCreateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            group = await self.uow.group.create(obj=create_obj)
            await self.uow.group.user_add(
                obj=UserGroupCreateDTO(user_id=user.id, group_id=group.id, role=GroupRoleEnum.SUPERUSER)
            )
            await uow.commit()
        return Result(item=group)
