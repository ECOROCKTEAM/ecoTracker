from dataclasses import dataclass
from src.core.entity.user import User

from src.core.exception.mission import MissionDeactivatedError
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.mission import IRepositoryMission
from src.core.entity.mission import Mission


@dataclass
class Result:
    item: Mission


class MissionGetUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        mission = await self.repo.get(id=id)
        if not mission.active:
            raise MissionDeactivatedError(mission_id=mission.id)
        return Result(item=mission)
