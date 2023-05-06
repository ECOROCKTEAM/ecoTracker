from dataclasses import dataclass
from src.core.entity.user import User

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.entity.mission import MissionCommunity
from src.core.dto.challenges.mission import MissionCommunityCreateDTO


@dataclass
class Result:
    item: MissionCommunity


class MissionCommunityCreateUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, create_obj: MissionCommunityCreateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        mission = await self.repo.community_mission_create(obj=create_obj, return_language=user.language)
        return Result(item=mission)
