from dataclasses import dataclass
from src.core.entity.user import User

from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.entity.mission import MissionBase, MissionUpdateDTO


@dataclass
class Result:
    item: MissionBase


class MissionUpdateUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, update_obj: MissionUpdateDTO) -> Result:
        mission = await self.repo.update(obj=update_obj)
        return Result(item=mission)
