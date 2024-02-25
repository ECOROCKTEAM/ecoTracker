from dataclasses import dataclass

from src.core.dto.group.score import GroupRatingDTO
from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: list[GroupRatingDTO]


class GroupGetRatingTopUsecase:
    # TODO NOT READY

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, *, user: User, group_id: int, size: int) -> Result:
        async with self.uow as uow:
            result = await uow.score_group.get_rating_top(size=size, group_privacy__in=[])

        return Result(item=result)
