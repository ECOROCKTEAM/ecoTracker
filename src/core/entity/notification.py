from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from src.core.enum.event import EventTypeEnum


@dataclass
class Notification:
    event_type: EventTypeEnum
    user_id: str | None = None
    meta: dict = field(default_factory=dict)  # example: {'id': 123, 'entity': 'task'}
    created_at: datetime = field(default_factory=datetime.now)
    viewed_at: datetime | None = None
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if self.event_type is not EventTypeEnum.NEW_ANNOUNCMENT and not self.user_id:
            raise ValueError("user_id is required for non-system notification")
