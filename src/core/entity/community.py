from dataclasses import dataclass
from datetime import datetime

from src.core.enum.community.privacy import CommunityPrivacyEnum


@dataclass
class Community:
    """Community entity"""

    id: int
    name: str
    description: str
    active: bool
    privacy: CommunityPrivacyEnum


@dataclass
class CommunityInvite:
    community_id: int
    code: str | None
    expire_time: datetime | None
