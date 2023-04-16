from dataclasses import dataclass

from src.core.interfaces.base import IRepositoryCore
from src.core.dto.occupancy import OccupancyStatusCreateDTO, OccupancyStatusDTO
from src.core.entity.user import User
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: OccupancyStatusDTO


class OccupancyStatusCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: OccupancyStatusCreateDTO) -> Result:
        
        if not user.application_role.ADMIN:
            raise UserPermissionError
        
        occupancy_status = self.repo.occupancy_status_create(obj=obj)

        return Result(item=occupancy_status)

