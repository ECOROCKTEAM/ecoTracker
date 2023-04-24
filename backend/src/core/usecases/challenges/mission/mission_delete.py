from dataclasses import dataclass
from src.core.entity.user import User

from src.core.exception.user import UserPermissionError
from src.core.interfaces.repository.mission import IRepositoryMission


@dataclass
class Result:
    item: int


class MissionDeleteUsecase:
    def __init__(self, *, repo: IRepositoryMission) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)
        rm_id = await self.repo.deactivate(id=id)
        return Result(item=rm_id)
