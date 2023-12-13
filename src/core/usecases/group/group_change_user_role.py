from dataclasses import dataclass

from src.core.dto.m2m.user.group import UserGroupDTO, UserGroupUpdateDTO
from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive, EntityNotFound
from src.core.exception.user import PermissionError, UserIsNotPremiumError
from src.core.interfaces.repository.group.group import GroupUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: UserGroupDTO


class GroupChangeUserRoleUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, group_id: int, user_id: str, update_obj: UserGroupUpdateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            group = await uow.group.get(id=group_id)
            if not group.active:
                raise EntityNotActive(msg=f"{group.id=}")
            # that part looks like this for can be tested!
            # old realization with 2 .get methods not can be tested
            group_users = await uow.group.user_list(
                id=group.id, filter_obj=GroupUserFilter(user_id__in=[user.id, user_id])
            )
            current_user = None
            target_user = None

            for group_user in group_users:
                if group_user.user_id == user.id:
                    current_user = group_user
                if group_user.user_id == user_id:
                    target_user = group_user

            if current_user is None:
                raise EntityNotFound(msg=f"Not found current user user_id={user.id}")
            if target_user is None:
                raise EntityNotFound(msg=f"Not found target user user_id={user_id}")
            if current_user.role not in (GroupRoleEnum.SUPERUSER, GroupRoleEnum.ADMIN):
                raise PermissionError(msg=f"current user is not administrator: user_id={user.id}, {group_id=}")

            if target_user.role == GroupRoleEnum.SUPERUSER and current_user.role != GroupRoleEnum.SUPERUSER:
                raise PermissionError(msg=f"current user is not superuser: user_id={user.id}, {group_id=}")
            link = await uow.group.user_role_update(obj=update_obj, group_id=group_id, user_id=user_id)
            await uow.commit()
        return Result(item=link)
