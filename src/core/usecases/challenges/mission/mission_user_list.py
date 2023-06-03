from dataclasses import dataclass

from src.core.dto.mock import MockObj
from src.core.entity.mission import MissionUser
from src.core.entity.user import User
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.challenges.mission import MissionUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: list[MissionUser]


class MissionUserListUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self, *, user: User, filter_obj: MissionUserFilter, order_obj: MockObj, pagination_obj: MockObj
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            mission_list = await uow.mission.user_mission_lst(
                user_id=user.id, filter_obj=filter_obj, order_obj=order_obj, pagination_obj=pagination_obj
            )
        return Result(item=mission_list)
