from dataclasses import dataclass, field

from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.user import User
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive, PrivacyError
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.group.group import GroupUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[UserGroupDTO] = field(default_factory=list)


class GroupUserListUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, user: User, group_id: int, filter_obj: GroupUserFilter) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            group = await uow.group.get(id=group_id)
            if not group.active:
                raise EntityNotActive(msg=f"{group.id}")
            user_grop_list = await uow.group.user_list(id=group_id, filter_obj=filter_obj)

            user_in_group = False
            for user_group in user_grop_list:
                if user_group.user_id == user.id and user_group.role == GroupRoleEnum.BLOCKED:
                    raise PermissionError(f"{user.id=} BLOCKED in {user_group.group_id=}")
                if user_group.user_id == user.id:
                    user_in_group = True
                    break

            if group.privacy == GroupPrivacyEnum.PRIVATE and not user_in_group:
                raise PrivacyError(msg=f"{user.id=} not in {group_id=} and {group_id=} is {GroupPrivacyEnum.PRIVATE}")

        return Result(items=user_grop_list)
