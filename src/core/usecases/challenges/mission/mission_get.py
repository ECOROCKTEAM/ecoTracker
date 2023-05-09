from dataclasses import dataclass
from src.core.entity.user import User

from src.core.exception.mission import MissionDeactivatedError
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.entity.mission import Mission


@dataclass
class Result:
    item: Mission


class MissionGetUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        mission = await self.repo.get(id=id, lang=user.language)
        if not mission.active:
            raise MissionDeactivatedError(user_id=user.id)
        return Result(item=mission)
