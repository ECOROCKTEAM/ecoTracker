from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.application.database.base import Base
from src.core.enum.event import EventTypeEnum


@dataclass
class NotificationModel(Base):
    __tablename__ = "notifications"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=func.uuid_generate_v4())
    user_id: Mapped[str | None] = mapped_column(
        ForeignKey("user.id"), nullable=True
    )  # if no user_id, it's system notification
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    viewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, nullable=True)
    event_type: Mapped[EventTypeEnum] = mapped_column(nullable=False)
    meta: Mapped[dict[str, Any]] = mapped_column()  # example: {'id': 123, 'entity': 'task'}
