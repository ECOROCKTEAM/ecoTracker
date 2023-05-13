from dataclasses import dataclass

from src.core.dto.challenges.mission import MissionUserCreateDTO
from src.core.entity.mission import MissionUser
from src.core.entity.user import User
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.challenges.mission import IRepositoryMission


@dataclass
class Result:
    item: MissionUser


class MissionUserCreateUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, create_obj: MissionUserCreateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        mission = await self.repo.user_mission_create(obj=create_obj, lang=user.language)
        return Result(item=mission)
