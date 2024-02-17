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

            privileged_roles = (GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER)

            if group.privacy == GroupPrivacyEnum.PUBLIC:
                if not group.active:
                    raise EntityNotActive(msg=f"{group.id}")

                if user_group.role not in privileged_roles or not user_group:
                    if not filter_obj.role__in:
                        filter_obj.role__in = [GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER, GroupRoleEnum.USER]
                    elif GroupRoleEnum.BLOCKED in filter_obj.role__in:
                        raise PermissionError(msg=f"{user.id=} can not see BLOCKED users in group")

                    result = await uow.group.user_list(id=group_id, filter_obj=filter_obj)

                elif user_group.role in privileged_roles:
                    result = await uow.group.user_list(id=group_id, filter_obj=filter_obj)

            if group.privacy == GroupPrivacyEnum.PRIVATE:
                if not user_group:
                    raise PermissionError(msg=f"{user.id=} not in group")

                if not group.active:
                    raise EntityNotActive(msg=f"{group.id}")

                if user_group.role in privileged_roles:
                    result = await uow.group.user_list(id=group_id, filter_obj=filter_obj)

                elif user_group.role not in privileged_roles:
                    if not filter_obj.role__in:
                        filter_obj.role__in = [GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER, GroupRoleEnum.USER]
                    elif GroupRoleEnum.BLOCKED in filter_obj.role__in:
                        raise PermissionError(msg=f"{user.id=} can not see BLOCKED users in group")

                    result = await uow.group.user_list(id=group_id, filter_obj=filter_obj)

        return Result(items=result)
