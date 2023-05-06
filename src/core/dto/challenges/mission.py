from dataclasses import dataclass

from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class MissionUserCreateDTO:
    username: str
    mission_id: int
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE


@dataclass
class MissionUserUpdateDTO:
    id: int
    status: OccupancyStatusEnum | None = None


@dataclass
class MissionCommunityCreateDTO:
    mission_id: int
    community_id: str
    author: str
    place: str | None = None
    meeting_date: int | None = None
    people_required: int | None = None
    people_max: int | None = None
    comment: str | None = None
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE


@dataclass
class MissionCommunityUpdateDTO:
    id: int
    status: OccupancyStatusEnum | None = None
    place: str | None = None
    meeting_date: int | None = None
    people_required: int | None = None
    people_max: int | None = None
    comment: str | None = None
