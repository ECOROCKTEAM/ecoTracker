from dataclasses import dataclass

from src.core.dto.utils import IterableObj
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.group.group import GroupFilter, SortingGroupObj
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: list[Group]
    limit: int | None
    offset: int
    total: int


class GroupListUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self, *, user: User, filter_obj: GroupFilter, sorting_obj: SortingGroupObj, iterable_obj: IterableObj
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        filter_obj.active = True
        async with self.uow as uow:
            group_list = await uow.group.lst(filter_obj=filter_obj, sorting_obj=sorting_obj, iterable_obj=iterable_obj)
        return Result(item=group_list.items, limit=group_list.limit, offset=group_list.offset, total=group_list.total)
