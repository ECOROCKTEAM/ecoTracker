from dataclasses import dataclass
from src.core.entity.user import User

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.mission import IRepositoryMission
from src.core.entity.mission import MissionCommunity, MissionCommunityUpdateDTO


@dataclass
class Result:
    item: MissionCommunity


class MissionCommunityUpdateUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, update_obj: MissionCommunityUpdateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        mission = await self.repo.update_for_community(obj=update_obj)
        return Result(item=mission)
