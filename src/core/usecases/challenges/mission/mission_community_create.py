from dataclasses import dataclass

from src.core.dto.challenges.mission import MissionCommunityCreateDTO
from src.core.entity.mission import MissionCommunity
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: MissionCommunity


class MissionCommunityCreateUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, create_obj: MissionCommunityCreateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            user_community = await uow.community.user_get(community_id=create_obj.community_id, user_id=user.id)
            if user_community.role in [CommunityRoleEnum.USER, CommunityRoleEnum.BLOCKED]:
                raise PermissionError("")
            mission = await uow.mission.community_mission_create(obj=create_obj)
            await uow.commit()
        return Result(item=mission)
