from dataclasses import dataclass

from src.core.interfaces.base import IRepositoryCore
from src.core.dto.occupancy import OccupancyTypeCreateDTO, OccupancyTypeDTO
from src.core.entity.user import User
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: OccupancyTypeDTO


class OccupancyTypeCreateUseCase:
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: OccupancyTypeCreateDTO) -> Result:
        if not user.application_role.ADMIN:
            raise UserPermissionError(username=user.username)

        occupancy_type = await self.repo.occupancy_type_create(obj=obj)

        return Result(item=occupancy_type)
