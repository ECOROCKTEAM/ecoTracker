from dataclasses import dataclass

from src.core.dto.challenges.mission import MissionUserUpdateDTO
from src.core.dto.user.score import AddScoreUserDTO
from src.core.entity.mission import MissionUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.exception.base import EntityNotChange
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: MissionUser


class MissionUserUpdateUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int, update_obj: MissionUserUpdateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            user_mission = await uow.mission.user_mission_get(id=id, user_id=user.id)
            if user_mission.status != OccupancyStatusEnum.ACTIVE:
                raise EntityNotChange(msg="")
            updated_user_mission = await uow.mission.user_mission_update(id=id, user_id=user.id, obj=update_obj)
            if update_obj.status == OccupancyStatusEnum.FINISH:
                base_mission = await uow.mission.get(id=user_mission.mission_id, lang=user.language)
                score = await uow.score_user.add(
                    obj=AddScoreUserDTO(user_id=user.id, value=base_mission.score, operation=ScoreOperationEnum.PLUS)
                )
                if score.user_id != user.id:
                    raise EntityNotChange(msg="")
            await uow.commit()
        return Result(item=updated_user_mission)
