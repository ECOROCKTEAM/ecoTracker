from dataclasses import dataclass
from src.core.entity.user import User

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.mission import IRepositoryMission
from src.core.entity.mission import MissionUser, MissionUserCreateDTO


@dataclass
class Result:
    item: MissionUser


class MissionUserCreateUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, create_obj: MissionUserCreateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        mission = await self.repo.create_for_user(obj=create_obj)
        return Result(item=mission)
