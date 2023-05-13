from dataclasses import dataclass

from src.core.entity.mission import MissionCommunity
from src.core.entity.user import User
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.challenges.mission import IRepositoryMission


@dataclass
class Result:
    item: MissionCommunity


class MissionCommunityGetUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        mission = await self.repo.community_mission_get(id=id, lang=user.language)
        return Result(item=mission)
