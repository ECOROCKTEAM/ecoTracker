from dataclasses import dataclass
from datetime import datetime


@dataclass
class GroupInviteDTO:
    group_id: int
    code: str | None
    expire_time: datetime | None


@dataclass
class GroupInviteUpdateDTO:
    code: str
    expire_time: datetime
