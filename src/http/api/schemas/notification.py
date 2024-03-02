from datetime import datetime
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel

from src.core.entity.notification import Notification
from src.core.enum.event import EventTypeEnum
from src.core.interfaces.repository.notifications.notifications import (
    NotificationFilter,
)


class NotificationFilterSchema(BaseModel):
    from_: datetime | None = Query(alias="from", default=None)
    to_: datetime | None = Query(alias="to", default=None)
    viewed: bool | None = Query(default=None)

    def to_obj(self) -> NotificationFilter:
        return NotificationFilter(
            from_=self.from_,
            to_=self.to_,
            viewed=self.viewed,
        )


class NotificationSchema(BaseModel):
    event_type: EventTypeEnum
    meta: dict
    user_id: str | None
    created_at: datetime
    viewed_at: datetime | None
    id: UUID

    @classmethod
    def from_obj(cls, notification: Notification) -> "NotificationSchema":
        return cls(
            id=notification.id,
            user_id=notification.user_id,
            meta=notification.meta,
            created_at=notification.created_at,
            event_type=notification.event_type,
            viewed_at=notification.viewed_at,
        )


class NotificationListSchema(BaseModel):
    items: list[NotificationSchema]

    @classmethod
    def from_obj(cls, notification_list: list[Notification]) -> "NotificationListSchema":
        items = [NotificationSchema.from_obj(notification=notification) for notification in notification_list]
        return cls(items=items)


class NotificationCountSchema(BaseModel):
    count: int


class NotificationIdListSchema(BaseModel):
    ids: list[UUID]
