from dataclasses import dataclass

from src.core.entity.occupancy import OccupancyCategory
from src.core.entity.user import User
from src.core.exception.user import UserNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: OccupancyCategory


class CategoryGetUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            category = await uow.occupancy_category.get(id=id, lang=user.language)

        return Result(item=category)
