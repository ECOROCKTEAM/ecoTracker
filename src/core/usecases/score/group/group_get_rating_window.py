from dataclasses import dataclass

from src.core.dto.group.score import GroupRatingDTO
from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.score.group.access_functions import access_check_target_group


@dataclass
class Result:
    item: list[GroupRatingDTO]


class GroupGetRatingWindowUsecase:
    # TODO NOT READY

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, *, user: User, group_id: int, window_offset: int) -> Result:
        async with self.uow as uow:
            await access_check_target_group(uow=uow, user=user, group_id=group_id)
            result = await uow.score_group.get_rating_window(
                window_offset=window_offset, group_id=group_id, group_privacy__in=[]
            )

        return Result(item=result)
