from dataclasses import dataclass

from src.core.dto.mock import MockObj
from src.core.dto.user.score import UserBoundOffsetDTO, UserScoreDTO
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError, UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    # Dict with user rating as a key and user DTO as a value
    items: list[UserScoreDTO]


class UserGetRatingUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, *, user: User, order_obj: MockObj, bound_offset: int | None = None) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id, deactivated=user.active)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            if bound_offset is not None:
                """Get rating for specific user."""

                obj = UserBoundOffsetDTO(user_id=user.id, bound_offset=bound_offset)
                rating = await uow.score_user.user_rating(obj=obj, order_obj=order_obj)
            else:
                """Global user rating"""

                rating = await uow.score_user.user_rating(order_obj=order_obj)

        return Result(items=rating)
