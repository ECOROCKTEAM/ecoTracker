from dataclasses import dataclass

from src.core.entity.user import User
from src.core.exception.user import UserNotActive
from src.core.interfaces.repository.notifications.notifications import (
    NotificationFilter,
)
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: int


class GetUnreadNotificationsCountUsecase:
    """
    Get unread notifications count for user
    """

    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        filter_obj = NotificationFilter(viewed=False)
        async with self.uow as uow:
            count = await uow.notifications.count(user_id=user.id, filter_obj=filter_obj)

        return Result(item=count)
