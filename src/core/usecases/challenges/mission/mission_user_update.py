from dataclasses import dataclass
from src.core.entity.user import User

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.entity.mission import MissionUser
from src.core.dto.challenges.mission import MissionUserUpdateDTO


@dataclass
class Result:
    item: MissionUser


class MissionUserUpdateUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, update_obj: MissionUserUpdateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        mission = await self.repo.user_mission_update(obj=update_obj, lang=user.language)
        return Result(item=mission)
