from dataclasses import dataclass, field

from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.user import User
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive
from src.core.exception.user import (
    PermissionError,
    UserIsNotActivateError,
    UserIsNotPremiumError,
)
from src.core.interfaces.repository.group.group import GroupUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[UserGroupDTO] = field(default_factory=list)


class GroupUserListUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, user: User, group_id: int, filter_obj: GroupUserFilter) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            user_group = await uow.group.user_get(group_id=group_id, user_id=user.id)
            if user_group.role == GroupRoleEnum.BLOCKED:
                raise PermissionError(msg=f"{user.id=} is BLOCKED")

            group = await uow.group.get(id=group_id)

            if group.privacy == GroupPrivacyEnum.PUBLIC:
                if not group.active:
                    raise EntityNotActive(msg=f"{group.id}")

                if user_group.role not in (GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER) or not user_group:
                    filter_obj.role__in = [GroupRoleEnum.USER]
                    result = await uow.group.user_list(id=group_id, filter_obj=filter_obj)

                if user_group.role in (GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER):
                    result = await uow.group.user_list(id=group_id, filter_obj=filter_obj)

            if group.privacy == GroupPrivacyEnum.PRIVATE:
                if not user_group:
                    raise PermissionError(msg=f"{user.id=} not in group")

                if not group.active:
                    raise EntityNotActive(msg=f"{group.id}")

                if user_group.role in (GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER):
                    result = await uow.group.user_list(id=group_id, filter_obj=filter_obj)
                if user_group.role == GroupRoleEnum.USER:
                    filter_obj.role__in = [GroupRoleEnum.USER]
                    result = await uow.group.user_list(id=group_id, filter_obj=filter_obj)

        return Result(items=result)
