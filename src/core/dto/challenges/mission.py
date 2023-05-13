from dataclasses import dataclass
from datetime import datetime

from src.core.dto.base import UpdateDTO
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.typing.base import UNSET, UnsetType


@dataclass
class MissionUserCreateDTO:
    user_id: int
    mission_id: int
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE


@dataclass
class MissionUserUpdateDTO(UpdateDTO):
    status: OccupancyStatusEnum | UnsetType = UNSET


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
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE


@dataclass
class MissionCommunityUpdateDTO(UpdateDTO):
    status: OccupancyStatusEnum | UnsetType = UNSET
    place: str | UnsetType = UNSET
    meeting_date: datetime | UnsetType = UNSET
    people_required: int | UnsetType = UNSET
    people_max: int | UnsetType = UNSET
    comment: str | UnsetType = UNSET
