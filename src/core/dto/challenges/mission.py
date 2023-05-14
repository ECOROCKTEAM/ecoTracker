from dataclasses import dataclass, field
from datetime import datetime

from src.core.dto.base import UpdateDTO
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.typing.base import UNSET, UnsetType


@dataclass
class MissionUserCreateDTO:
    mission_id: int
    date_close: datetime | None = field(init=False, default=None)
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE


@dataclass
class MissionUserUpdateDTO(UpdateDTO):
    date_close: datetime | UnsetType = field(init=False, default=UNSET)
    status: OccupancyStatusEnum | UnsetType = UNSET

    def __post_init__(self):
        if self.status == OccupancyStatusEnum.FINISH:
            self.date_close = datetime.now()


@dataclass
class MissionCommunityCreateDTO:
    mission_id: int
    community_id: int
    author: str
    place: str | None = None
    meeting_date: datetime | None = None
    people_required: int | None = None
    people_max: int | None = None
    comment: str | None = None
    date_close: datetime | None = field(init=False, default=None)
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE


@dataclass
class MissionCommunityUpdateDTO(UpdateDTO):
    date_close: datetime | UnsetType = field(init=False, default=UNSET)
    status: OccupancyStatusEnum | UnsetType = UNSET
    place: str | UnsetType = UNSET
    meeting_date: datetime | UnsetType = UNSET
    people_required: int | UnsetType = UNSET
    people_max: int | UnsetType = UNSET
    comment: str | UnsetType = UNSET

    def __post_init__(self):
        if self.status == OccupancyStatusEnum.FINISH:
            self.date_close = datetime.now()
