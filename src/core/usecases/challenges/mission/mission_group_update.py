from dataclasses import dataclass

from src.core.dto.challenges.mission import MissionGroupUpdateDTO
from src.core.dto.group.score import GroupOperationWithScoreDTO
from src.core.entity.mission import MissionGroup
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.exception.base import EntityNotActive, EntityNotChange
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: MissionGroup


class MissionGroupUpdateUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int, group_id: int, update_obj: MissionGroupUpdateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            group = await uow.group.get(id=group_id)
            if not group.active:
                raise EntityNotActive(msg="")

            user_group = await uow.group.user_get(group_id=group_id, user_id=user.id)
            if user_group.role in [GroupRoleEnum.USER, GroupRoleEnum.BLOCKED]:
                raise PermissionError("")

            group_mission = await uow.mission.group_mission_get(id=id, group_id=group_id)
            if group_mission.status != OccupancyStatusEnum.ACTIVE:
                raise EntityNotChange(msg="")

            updated_group_mission = await uow.mission.group_mission_update(id=id, group_id=group_id, obj=update_obj)
            if update_obj.status == OccupancyStatusEnum.FINISH:
                base_mission = await uow.mission.get(id=group_mission.mission_id, lang=user.language)
                score = await uow.score_group.add(
                    obj=GroupOperationWithScoreDTO(
                        group_id=group_id, value=base_mission.score, operation=ScoreOperationEnum.PLUS
                    )
                )
                if score.group_id != group_id:
                    raise EntityNotChange(msg="")
            await uow.commit()
        return Result(item=updated_group_mission)
