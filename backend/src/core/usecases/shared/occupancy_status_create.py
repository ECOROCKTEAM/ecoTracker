from dataclasses import dataclass

from src.core.dto.challenges.status  import OccupancyStatusCreateDTO, OccupancyStatusDTO
from src.core.interfaces.challenges.occupancy.occupancy import IOccupancyRepository
from src.core.entity.user import User
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: OccupancyStatusDTO


class OccupancyStatusCreateUseCase:
    def __init__(self, repo: IOccupancyRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: OccupancyStatusCreateDTO) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError

        status = await self.repo.status_create(obj=obj)
        return Result(item=status)
