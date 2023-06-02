from dataclasses import dataclass
from datetime import datetime


@dataclass
class CommunityInviteDTO:
    community_id: int
    code: str | None
    expire_time: datetime | None


@dataclass
class CommunityInviteUpdateDTO:
    code: str
    expire_time: datetime
