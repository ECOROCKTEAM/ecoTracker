from dataclasses import dataclass

from src.core.dto.mock import MockObj
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.group.group import GroupFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: list[Group]


class GroupListUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self, *, user: User, filter_obj: GroupFilter, order_obj: MockObj, pagination_obj: MockObj
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        filter_obj.active = True
        async with self.uow as uow:
            group_list = await uow.group.lst(filter_obj=filter_obj, order_obj=order_obj, pagination_obj=pagination_obj)
        return Result(item=group_list)