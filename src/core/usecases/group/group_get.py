from dataclasses import dataclass

from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import (
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

    async def __call__(self, *, user: User, group_id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            group = await uow.group.get(id=group_id)

            try:
                group_user = await uow.group.user_get(group_id=group_id, user_id=user.id)
                if group_user.role != GroupRoleEnum.SUPERUSER and not group.active:
                    raise PermissionError(msg=f"{user.id}")

            except EntityNotFound as err:
                if group.privacy == GroupPrivacyEnum.PRIVATE:
                    raise PrivacyError(msg=f"{group_id=}") from err
                if not group.active:
                    raise EntityNotActive(msg=f"{group_id=}") from err

            return Result(item=group)
