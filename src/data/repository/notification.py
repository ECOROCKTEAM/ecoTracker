from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entity.notification import Notification
from src.core.enum.language import LanguageEnum
from src.core.interfaces.repository.notifications.notifications import (
    INotificationRepository,
    NotificationFilter,
)
from src.data.models.notification.notification import NotificationModel


def model_to_dto(model: NotificationModel) -> Notification:
    return Notification(
        id=model.id,
        user_id=model.user_id,
        created_at=model.created_at,
        viewed_at=model.viewed_at,
        event_type=model.event_type,
        meta=model.meta,
    )


def model_from_dto(dto: Notification) -> NotificationModel:
    return NotificationModel(
        id=dto.id,
        user_id=dto.user_id,
        created_at=dto.created_at,
        event_type=dto.event_type,
        meta=dto.meta,
        viewed_at=dto.viewed_at,
    )


class NotificationRepository(INotificationRepository):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def add(self, notification: Notification) -> Notification:
        notification_model = model_from_dto(notification)
        self.db_context.add(notification_model)
        await self.db_context.flush()
        return model_to_dto(notification_model)

    async def lst(self, *, user_id: str, filter_obj: NotificationFilter, lang: LanguageEnum) -> list[Notification]:
        stmt = select(NotificationModel).where(
            NotificationModel.user_id == user_id or NotificationModel.user_id.is_(None)
        )
        if filter_obj.from_ is not None:
            stmt = stmt.where(NotificationModel.created_at >= filter_obj.from_)
        if filter_obj.to_ is not None:
            stmt = stmt.where(NotificationModel.created_at <= filter_obj.to_)
        if filter_obj.viewed is True:
            stmt = stmt.where(NotificationModel.viewed_at.isnot(None))
        if filter_obj.viewed is False:
            stmt = stmt.where(NotificationModel.viewed_at.is_(None))

        res = await self.db_context.scalars(stmt)
        return [model_to_dto(models) for models in res]

    async def count(self, *, user_id: str, filter_obj: NotificationFilter, lang: LanguageEnum) -> int:
        stmt = select(func.count("*")).select_from(NotificationModel).where(NotificationModel.user_id == user_id)
        if filter_obj.from_ is not None:
            stmt = stmt.where(NotificationModel.created_at >= filter_obj.from_)
        if filter_obj.to_ is not None:
            stmt = stmt.where(NotificationModel.created_at <= filter_obj.to_)
        if filter_obj.viewed is not None:
            stmt = stmt.where(NotificationModel.viewed_at.is_not(None))

        notifications_count = await self.db_context.scalar(stmt)
        return notifications_count or 0

    async def mark_as_viewed(self, *, user_id: str, ids: list[UUID]) -> list[UUID]:
        stmt = (
            update(NotificationModel)
            .where(NotificationModel.id.in_(ids), NotificationModel.user_id == user_id)
            .returning(NotificationModel.id)
            .values(viewed_at=datetime.now())
        )
        updated_ids = await self.db_context.scalars(stmt)
        return list(updated_ids)
