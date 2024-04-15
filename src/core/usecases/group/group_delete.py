from dataclasses import dataclass

from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotFound, PermissionError
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: int


class GroupDeleteUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, group_id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            try:
                user_role = await uow.group.user_get(group_id=group_id, user_id=user.id)
            # raised EntityNotFound if user is not member
            except EntityNotFound as err:
                raise PermissionError(msg=f"{user.id=}") from err

            if user_role.role != GroupRoleEnum.SUPERUSER:
                raise PermissionError(msg=f"{user.username=}, {group_id=}")

            deactivate_id = await uow.group.deactivate(id=group_id)
            await uow.commit()
            return Result(item=deactivate_id)
