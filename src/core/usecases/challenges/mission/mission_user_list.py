from dataclasses import dataclass

from src.core.dto.mock import MockObj
from src.core.entity.user import User

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.challenges.mission import IRepositoryMission, MissionUserFilter
from src.core.entity.mission import MissionUser


@dataclass
class Result:
    item: list[MissionUser]


class MissionUserListUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(
        self, *, user: User, filter_obj: MissionUserFilter, order_obj: MockObj, pagination_obj: MockObj
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        mission_list = await self.repo.user_mission_lst(
            filter_obj=filter_obj, order_obj=order_obj, pagination_obj=pagination_obj, return_language=user.language
        )
        return Result(item=mission_list)
