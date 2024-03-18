from dataclasses import dataclass
from uuid import UUID

from src.core.entity.user import User
from src.core.exception.user import UserNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: list[UUID]


class MarkNotificationsAsViewedUsecase:
    """
    Mark notifications as viewed
    """

    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, ids: list[UUID]) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            updated_ids = await uow.notifications.mark_as_viewed(user_id=user.id, ids=ids)

        return Result(item=updated_ids)
