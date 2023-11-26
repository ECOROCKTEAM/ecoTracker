from dataclasses import dataclass

from src.core.dto.group.score import GroupBoundOffsetDTO, GroupRatingDTO
from src.core.dto.mock import MockObj
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError, UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    # Dict with group rating as a key and group DTO as a value
    item: list[GroupRatingDTO]


class GroupGetRatingUsecase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(
        self,
        *,
        user: User,
        order_obj: MockObj,
        group_id: int | None = None,
        bound_offset: int | None = None,
    ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id, deactivated=user.active)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            if group_id is not None:
                """Get rating for specific group"""

                obj = GroupBoundOffsetDTO(group_id=group_id, bound_offset=bound_offset)  # type: ignore
                rating = await uow.score_group.group_rating(
                    order_obj=order_obj,
                    obj=obj,
                )

            else:
                """Get global group rating."""

                rating = await uow.score_group.group_rating(order_obj=order_obj)

            return Result(item=rating)
