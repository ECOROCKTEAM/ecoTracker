from dataclasses import dataclass
from src.core.entity.user import User

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.mission import IRepositoryMission
from src.core.entity.mission import MissionUser, MissionUserUpdateDTO


@dataclass
class Result:
    item: MissionUser


class MissionUserUpdateUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, update_obj: MissionUserUpdateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        mission = await self.repo.update_for_user(obj=update_obj)
        return Result(item=mission)
