from dataclasses import dataclass
from datetime import datetime

from src.core.enum.group.privacy import GroupPrivacyEnum


@dataclass
class Group:
    """Group entity"""

    id: int
    name: str
    description: str
    active: bool
    privacy: GroupPrivacyEnum


@dataclass
class GroupInvite:
    group_id: int
    code: str | None
    expire_time: datetime | None
