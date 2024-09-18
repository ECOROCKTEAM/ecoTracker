from dataclasses import dataclass

from src.core.dto.utils import IterableObj
from src.core.entity.mission import MissionGroup
from src.core.entity.user import User
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.challenges.mission import (
    MissionGroupFilter,
    SortGroupMissionObj,
)
from src.core.interfaces.repository.group.group import GroupFilter, SortingGroupObj
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[MissionGroup]
    limit: int | None
    offset: int
    total: int


class MissionGroupListUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self,
        *,
        user: User,
        filter_obj: MissionGroupFilter,
        sorting_obj: SortGroupMissionObj,
        iterable_obj: IterableObj,
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            group_list = await uow.group.lst(
                filter_obj=GroupFilter(user_id=user.id, active=True),
                sorting_obj=SortingGroupObj(),
                iterable_obj=iterable_obj,
            )
            filter_obj.group_id_list = [item.id for item in group_list.items]
            res = await uow.mission.group_mission_lst(
                filter_obj=filter_obj, sorting_obj=sorting_obj, iterable_obj=iterable_obj
            )
        return Result(items=res.items, limit=res.limit, offset=res.offset, total=res.total)
