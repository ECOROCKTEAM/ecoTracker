from dataclasses import dataclass

from src.core.dto.utils import IterableObj
from src.core.entity.mission import MissionUser
from src.core.entity.user import User
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.challenges.mission import (
    MissionUserFilter,
    SortUserMissionObj,
)
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[MissionUser]
    limit: int | None
    offset: int
    total: int


class MissionUserListUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self,
        *,
        user: User,
        filter_obj: MissionUserFilter,
        sorting_obj: SortUserMissionObj,
        iterable_obj: IterableObj,
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            result = await uow.mission.user_mission_lst(
                user_id=user.id, filter_obj=filter_obj, sorting_obj=sorting_obj, iterable_obj=iterable_obj
            )
        return Result(items=result.items, offset=result.offset, limit=result.limit, total=result.total)
