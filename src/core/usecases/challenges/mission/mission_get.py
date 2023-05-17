from dataclasses import dataclass

from src.core.entity.mission import Mission
from src.core.entity.user import User
from src.core.exception.mission import MissionDeactivatedError
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: Mission


class MissionGetUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            mission = await uow.mission.get(id=id, lang=user.language)
        if not mission.active:
            raise MissionDeactivatedError(user_id=user.id)
        return Result(item=mission)
