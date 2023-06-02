from dataclasses import dataclass

from src.core.entity.mission import MissionUser
from src.core.entity.user import User
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: MissionUser


class MissionUserGetUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            user_mission = await uow.mission.user_mission_get(id=id, user_id=user.id)
        return Result(item=user_mission)
