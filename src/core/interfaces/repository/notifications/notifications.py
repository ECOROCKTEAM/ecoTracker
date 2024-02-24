from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.core.entity.notification import Notification


@dataclass
class NotificationFilter:
    """
    Filter object for notifications
    """

    from_: datetime | None = None
    to_: datetime | None = None
    viewed: bool | None = None


class INotificationRepository(ABC):
    """
    Interface for notification repository
    """

    @abstractmethod
    async def lst(self, *, user_id: str, filter_obj: NotificationFilter) -> list[Notification]:
        """Retrieve a list of notifications for a specific user.

        Args:
            user_id (str): The identifier of the user.
            filter_obj (NotificationFilter): The filter object for notifications.

        Returns:
            list[Notification]: A list of Notification entities.
        """

    @abstractmethod
    async def count(self, *, user_id: str, filter_obj: NotificationFilter) -> int:
        """Retrieve a count of notifications for a specific user.

        Args:
            user_id (str): The identifier of the user.
            filter_obj (NotificationFilter): The filter object for notifications.

        Returns:
            int: The count of notifications.
        """

    @abstractmethod
    async def mark_as_viewed(self, *, user_id: str, ids: list[UUID]) -> list[UUID]:
        """
        Mark notifications as viewed.

        Args:
            user_id (str): The identifier of the user.
            ids (list[UUID]): The identifiers of the notifications to mark as viewed.

        Returns:
            list[int]: The identifiers of the marked notifications.
        """
