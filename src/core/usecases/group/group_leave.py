from dataclasses import dataclass

from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import LogicError
from src.core.interfaces.repository.group.group import GroupUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: bool


class GroupLeaveUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, group_id: int) -> Result:
        async with self.uow as uow:
            group_user = await uow.group.user_get(group_id=group_id, user_id=user.id)
            if group_user.role == GroupRoleEnum.SUPERUSER:
                superuser_list = await uow.group.user_list(
                    id=group_id, filter_obj=GroupUserFilter(role__in=[GroupRoleEnum.SUPERUSER])
                )
                if len(superuser_list) == 1:
                    raise LogicError(msg=f"{user.id=}, {group_id=}")
            res = await uow.group.user_remove(group_id=group_id, user_id=user.id)
            await uow.commit()
        return Result(item=res)
