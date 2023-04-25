from dataclasses import dataclass

from src.core.dto.challenges.type import OccupancyTypeCreateDTO, OccupancyTypeDTO
from src.core.interfaces.challenges.occupancy.occupancy import IOccupancyRepository
from src.core.entity.user import User
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: OccupancyTypeDTO


class OccupancyTypeCreateUseCase:
    def __init__(self, repo: IOccupancyRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: OccupancyTypeCreateDTO) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        type = await self.repo.type_create(obj=obj)
        return Result(item=type)
