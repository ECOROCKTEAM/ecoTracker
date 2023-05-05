from dataclasses import dataclass
from src.core.entity.user import User

from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.entity.mission import MissionBase, MissionCreateDTO


@dataclass
class Result:
    item: MissionBase


class MissionCreateUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, create_obj: MissionCreateDTO) -> Result:
        mission = await self.repo.create(obj=create_obj)
        return Result(item=mission)
