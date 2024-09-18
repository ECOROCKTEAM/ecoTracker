from dataclasses import dataclass

from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import (
    DomainError,
    EntityNotActive,
    EntityNotFound,
    PermissionError,
    PrivacyError,
)
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: Group


class GroupGetUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def check_on_none_user(self, group: Group):
        if not group.active:
            raise EntityNotActive(msg=f"{group.id=}")
        if group.privacy == GroupPrivacyEnum.PRIVATE:
            raise PrivacyError(msg=f"{group.id=}")

    def check_on_exist_user(self, group: Group):
        if not group.active:
            raise EntityNotActive(msg=f"{group.id=}")

    async def __call__(self, *, user: User, group_id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            group = await uow.group.get(id=group_id)
            try:
                group_user = await uow.group.user_get(group_id=group_id, user_id=user.id)
            except EntityNotFound:
                group_user = None

            if group_user is None:
                self.check_on_none_user(group=group)
            elif group_user.role == GroupRoleEnum.USER:
                self.check_on_exist_user(group=group)
            elif group_user.role == GroupRoleEnum.BLOCKED:
                raise PermissionError(msg=f"{user.id}")
            elif group_user.role in (GroupRoleEnum.SUPERUSER, GroupRoleEnum.ADMIN):
                ...
            else:
                raise DomainError(msg="Something problem with roles!")

            return Result(item=group)
