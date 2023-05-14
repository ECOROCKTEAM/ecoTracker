from dataclasses import dataclass

from src.core.dto.challenges.mission import MissionUserUpdateDTO
from src.core.entity.mission import MissionUser
from src.core.entity.user import User
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: MissionUser


class MissionUserUpdateUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, mission_id: int, update_obj: MissionUserUpdateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            mission = await uow.mission.user_mission_update(obj=update_obj, user_id=user.id, mission_id=mission_id)
            await uow.commit()
        return Result(item=mission)
