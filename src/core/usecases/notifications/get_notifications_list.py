from dataclasses import dataclass

from src.core.entity.notification import Notification
from src.core.entity.user import User
from src.core.exception.user import UserNotActive
from src.core.interfaces.repository.notifications.notifications import (
    NotificationFilter,
)
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: list[Notification]


class GetNotificationsListUsecase:
    """
    Get notifications list for user
    """

    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, filter_obj: NotificationFilter) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            notifications = await uow.notifications.lst(user_id=user.id, filter_obj=filter_obj)

        return Result(item=notifications)
