from dataclasses import dataclass
from src.core.entity.user import User

from src.core.exception.user import UserPermissionError
from src.core.interfaces.repository.mission import IRepositoryMission
from src.core.entity.mission import Mission, MissionUpdateDTO


@dataclass
class Result:
    item: Mission


class MissionUpdateUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, update_obj: MissionUpdateDTO) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)
        mission = await self.repo.update(obj=update_obj)
        return Result(item=mission)
