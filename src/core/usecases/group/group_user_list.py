from dataclasses import dataclass, field

from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.user import User
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive, EntityNotFound
from src.core.exception.user import (
    PermissionError,
    UserIsNotPremiumError,
    UserNotActive,
)
from src.core.interfaces.repository.group.group import GroupUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[UserGroupDTO] = field(default_factory=list)


class GroupUserListUsecase:
    _PRIVILEGED_ROLES = (GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER)

    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, user: User, group_id: int, filter_obj: GroupUserFilter) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            group = await uow.group.get(id=group_id)
            if not group.active:
                raise EntityNotActive(msg=f"{group_id=}")

            try:
                user_group = await uow.group.user_get(group_id=group_id, user_id=user.id)
                if user_group.role == GroupRoleEnum.BLOCKED:
                    raise PermissionError(msg=f"{user.id=} is BLOCKED")
            except EntityNotFound:
                user_group = None

            if group.privacy == GroupPrivacyEnum.PUBLIC:
                filter_obj = await self._resolve_filter_public(user_group=user_group, filter_obj=filter_obj)
            elif group.privacy == GroupPrivacyEnum.PRIVATE:
                filter_obj = await self._resolve_filter_private(user_group=user_group, filter_obj=filter_obj)

        result = await self.uow.group.user_list(id=group_id, filter_obj=filter_obj)
        return Result(items=result)

    async def _resolve_filter_public(
        self, user_group: UserGroupDTO | None, filter_obj: GroupUserFilter
    ) -> GroupUserFilter:
        if user_group is None or user_group.role not in self._PRIVILEGED_ROLES:
            if not filter_obj.role__in:
                filter_obj.role__in = [GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER, GroupRoleEnum.USER]
            if GroupRoleEnum.BLOCKED in filter_obj.role__in:
                raise PermissionError(msg="User cannot see BLOCKED users in public group")
        return filter_obj

    async def _resolve_filter_private(
        self, user_group: UserGroupDTO | None, filter_obj: GroupUserFilter
    ) -> GroupUserFilter:
        if user_group is None:
            raise PermissionError(msg="User outside a private group cannot see any users in it")
        if user_group.role not in self._PRIVILEGED_ROLES:
            if not filter_obj.role__in:
                filter_obj.role__in = [GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER, GroupRoleEnum.USER]
            if GroupRoleEnum.BLOCKED in filter_obj.role__in:
                raise PermissionError(msg=f"user.id={user_group.user_id} cannot see BLOCKED users in private group")
        return filter_obj
