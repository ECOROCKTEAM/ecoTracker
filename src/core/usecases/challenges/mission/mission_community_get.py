from dataclasses import dataclass

from src.core.entity.mission import MissionCommunity
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.base import EntityNotActive
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: MissionCommunity


class MissionCommunityGetUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int, community_id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            user_community = await uow.community.user_get(community_id=community_id, user_id=user.id)
            if user_community.role in [CommunityRoleEnum.BLOCKED]:
                raise PermissionError("")
            community = await uow.community.get(id=community_id)
            if not community.active:
                raise EntityNotActive(msg="")
            community_mission = await uow.mission.community_mission_get(id=id, community_id=community_id)
        return Result(item=community_mission)
