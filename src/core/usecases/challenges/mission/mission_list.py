from dataclasses import dataclass
from src.core.entity.user import User

from src.core.dto.mock import MockObj
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.challenges.mission import IRepositoryMission, MissionFilter
from src.core.entity.mission import Mission


@dataclass
class Result:
    item: list[Mission]


class MissionListUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(
        self, *, user: User, filter_obj: MissionFilter, order_obj: MockObj, pagination_obj: MockObj
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        mission_list = await self.repo.lst(
            filter_obj=filter_obj, order_obj=order_obj, pagination_obj=pagination_obj, return_language=user.language
        )
        return Result(item=mission_list)
