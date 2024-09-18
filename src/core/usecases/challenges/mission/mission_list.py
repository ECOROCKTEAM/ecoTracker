from dataclasses import dataclass

from src.core.dto.utils import IterableObj
from src.core.entity.mission import Mission
from src.core.entity.user import User
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.challenges.mission import (
    MissionFilter,
    SortMissionObj,
)
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[Mission]
    limit: int | None
    offset: int
    total: int


class MissionListUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self, *, user: User, filter_obj: MissionFilter, sorting_obj: SortMissionObj, iterable_obj: IterableObj
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        filter_obj.active = True
        async with self.uow as uow:
            result = await uow.mission.lst(
                filter_obj=filter_obj, sorting_obj=sorting_obj, iterable_obj=iterable_obj, lang=user.language
            )
        return Result(items=result.items, total=result.total, offset=result.offset, limit=result.limit)
