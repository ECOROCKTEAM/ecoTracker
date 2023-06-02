from dataclasses import dataclass

from src.core.dto.challenges.mission import MissionCommunityUpdateDTO
from src.core.dto.community.score import CommunityOperationWithScoreDTO
from src.core.entity.mission import MissionCommunity
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.community.role import CommunityRoleEnum
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.exception.base import EntityNotActive, EntityNotChange
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: MissionCommunity


class MissionCommunityUpdateUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self, *, user: User, id: int, community_id: int, update_obj: MissionCommunityUpdateDTO
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            community = await uow.community.get(id=community_id)
            if not community.active:
                raise EntityNotActive(msg="")

            user_community = await uow.community.user_get(community_id=community_id, user_id=user.id)
            if user_community.role in [CommunityRoleEnum.USER, CommunityRoleEnum.BLOCKED]:
                raise PermissionError("")

            community_mission = await uow.mission.community_mission_get(id=id, community_id=community_id)
            if community_mission.status != OccupancyStatusEnum.ACTIVE:
                raise EntityNotChange(msg="")

            updated_community_mission = await uow.mission.community_mission_update(
                id=id, community_id=community_id, obj=update_obj
            )
            if update_obj.status == OccupancyStatusEnum.FINISH:
                base_mission = await uow.mission.get(id=community_mission.mission_id, lang=user.language)
                await uow.score_community.add(
                    obj=CommunityOperationWithScoreDTO(
                        community_id=community_id, value=base_mission.score, operation=ScoreOperationEnum.PLUS
                    )
                )
            await uow.commit()
        return Result(item=updated_community_mission)
