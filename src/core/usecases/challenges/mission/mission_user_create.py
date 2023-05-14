from dataclasses import dataclass

from src.core.dto.challenges.mission import MissionUserCreateDTO
from src.core.entity.mission import MissionUser
from src.core.entity.user import User
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: MissionUser


class MissionUserCreateUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, create_obj: MissionUserCreateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            mission = await uow.mission.user_mission_create(user_id=user.id, obj=create_obj)
            await uow.commit()
        return Result(item=mission)
