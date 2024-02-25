from dataclasses import dataclass

from src.core.dto.user.score import UserRatingDTO
from src.core.entity.user import User
from src.core.exception.user import UserNotActive, UserNotPremium
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: UserRatingDTO


class UserGetRatingUsecase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, *, user: User) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)
        if not user.is_premium:
            raise UserNotPremium(id=user.id)

        async with self.uow as uow:
            rating = await uow.score_user.get_rating(user_id=user.id)

        return Result(item=rating)
