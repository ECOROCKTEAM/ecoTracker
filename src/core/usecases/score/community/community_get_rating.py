from dataclasses import dataclass

from src.core.dto.community.score import CommunityBoundOffsetDTO, CommunityRatingDTO
from src.core.dto.mock import MockObj
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError, UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    # Dict with community rating as a key and community DTO as a value
    item: list[CommunityRatingDTO]


class CommunityGetRatingUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(
        self,
        *,
        user: User,
        order_obj: MockObj,
        community_id: int | None = None,
        bound_offset: int | None = None,
    ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id, deactivated=user.active)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            if community_id is not None:
                """Get rating for specific community"""

                obj = CommunityBoundOffsetDTO(community_id=community_id, bound_offset=bound_offset)  # type: ignore
                rating = await uow.score_community.community_rating(
                    order_obj=order_obj,
                    obj=obj,
                )

            else:
                """Get global community rating."""

                rating = await uow.score_community.community_rating(order_obj=order_obj)

            return Result(item=rating)
