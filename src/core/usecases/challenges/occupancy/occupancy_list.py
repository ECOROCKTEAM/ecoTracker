from dataclasses import dataclass

from src.core.entity.occupancy import OccupancyCategory
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[OccupancyCategory]


class OccupancyCategoryListUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        async with self.uow as uow:
            category_list = await uow.occupancy_category.lst(lang=user.language)

            return Result(items=category_list)
