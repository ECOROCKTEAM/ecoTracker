from dataclasses import dataclass

from src.core.dto.challenges.category import OccupancyCategoryCreateDTO, OccupancyCategoryDTO
from src.core.interfaces.repository.challenges.occupancy import IOccupancyRepository
from src.core.entity.user import User
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: OccupancyCategoryDTO


class OccupancyCategoryCreateUseCase:
    def __init__(self, repo: IOccupancyRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: OccupancyCategoryCreateDTO) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        type = await self.repo.type_create(obj=obj)
        return Result(item=type)
