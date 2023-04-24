from dataclasses import dataclass
from src.core.entity.user import User

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.mission import IRepositoryMission
from src.core.entity.mission import MissionCommunity


@dataclass
class Result:
    item: MissionCommunity


class MissionCommunityGetUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        mission = await self.repo.get_for_community(id=id)
        return Result(item=mission)
