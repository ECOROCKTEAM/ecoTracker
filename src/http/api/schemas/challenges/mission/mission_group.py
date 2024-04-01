from datetime import datetime

from pydantic import BaseModel

from src.core.dto.challenges.mission import MissionGroupCreateDTO, MissionGroupUpdateDTO
from src.core.entity.mission import MissionGroup
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.utils import SortType
from src.core.interfaces.repository.challenges.mission import (
    MissionGroupFilter,
    SortGroupMissionObj,
)


class MissionGroupFilterSchema(BaseModel):
    group_id: int | None = None
    group_id_list: list[int] | None = None
    mission_id: int | None = None
    status: OccupancyStatusEnum | None = None

    def to_obj(self) -> MissionGroupFilter:
        return MissionGroupFilter(
            group_id=self.group_id, group_id_list=self.group_id_list, mission_id=self.mission_id, status=self.status
        )


class MissionGroupSortingSchema(BaseModel):
    field: str = "mission_id"
    type: SortType = SortType.DESC

    def to_obj(self) -> SortGroupMissionObj:
        return SortGroupMissionObj(field=self.field, type=self.type)


class MissionGroupSchema(BaseModel):
    id: int
    group_id: int
    mission_id: int
    author: str
    date_start: datetime
    date_close: datetime | None
    status: OccupancyStatusEnum
    place: str | None = None
    meeting_date: datetime | None = None
    people_required: int | None = None
    people_max: int | None = None
    comment: str | None = None

    @classmethod
    def from_obj(cls, mission_group: MissionGroup) -> "MissionGroupSchema":
        return MissionGroupSchema(
            id=mission_group.id,
            group_id=mission_group.group_id,
            mission_id=mission_group.mission_id,
            author=mission_group.author,
            date_start=mission_group.date_start,
            date_close=mission_group.date_close,
            status=mission_group.status,
            place=mission_group.place,
            meeting_date=mission_group.meeting_date,
            people_required=mission_group.people_required,
            people_max=mission_group.people_max,
            comment=mission_group.comment,
        )


class MissionGroupListSchema(BaseModel):
    items: list[MissionGroupSchema]
    limit: int | None
    offset: int
    total: int

    @classmethod
    def from_obj(
        cls, mission_group_list: list[MissionGroup], limit: int | None, offset: int, total: int
    ) -> "MissionGroupListSchema":
        items = [MissionGroupSchema.from_obj(mission_group=mission_group) for mission_group in mission_group_list]
        return MissionGroupListSchema(items=items, limit=limit, offset=offset, total=total)


class MissionGroupCreateSchema(BaseModel):
    mission_id: int
    author: str
    place: str | None = None
    meeting_date: datetime | None = None
    people_required: int | None = None
    people_max: int | None = None
    comment: str | None = None

    def to_obj(self) -> MissionGroupCreateDTO:
        return MissionGroupCreateDTO(
            mission_id=self.mission_id,
            author=self.author,
            place=self.place,
            meeting_date=self.meeting_date,
            people_max=self.people_max,
            people_required=self.people_required,
            comment=self.comment,
        )


class MissionGroupUpdateSchema(BaseModel):
    status: OccupancyStatusEnum | None
    place: str | None
    meeting_date: datetime | None
    people_required: int | None
    people_max: int | None
    comment: str | None

    def to_obj(self) -> MissionGroupUpdateDTO:
        return MissionGroupUpdateDTO(
            status=self.status,
            place=self.place,
            meeting_date=self.meeting_date,
            people_required=self.people_required,
            people_max=self.people_max,
            comment=self.comment,
        )
