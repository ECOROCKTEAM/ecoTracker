from datetime import datetime

from pydantic import BaseModel

from src.core.dto.challenges.mission import MissionUserCreateDTO, MissionUserUpdateDTO
from src.core.entity.mission import MissionUser
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.utils import SortType
from src.core.interfaces.repository.challenges.mission import (
    MissionUserFilter,
    SortUserMissionObj,
)


class MissionUserUpdateSchema(BaseModel):
    status: OccupancyStatusEnum

    def to_obj(self) -> MissionUserUpdateDTO:
        return MissionUserUpdateDTO(status=self.status)


class MissionUserCreateSchema(BaseModel):
    mission_id: int
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE

    def to_obj(self) -> MissionUserCreateDTO:
        return MissionUserCreateDTO(mission_id=self.mission_id, status=self.status)


class MissionUserSchema(BaseModel):
    id: int
    user_id: str
    mission_id: int
    date_start: datetime
    date_close: datetime | None
    status: OccupancyStatusEnum

    @classmethod
    def from_obj(cls, mission_user: MissionUser) -> "MissionUserSchema":
        return MissionUserSchema(
            id=mission_user.id,
            user_id=mission_user.user_id,
            mission_id=mission_user.mission_id,
            date_close=mission_user.date_close,
            date_start=mission_user.date_start,
            status=mission_user.status,
        )


class MissionUserListSchema(BaseModel):
    items: list[MissionUserSchema]
    limit: int | None
    offset: int
    total: int

    @classmethod
    def from_obj(
        cls, mission_user_list: list[MissionUser], limit: int | None, offset: int, total: int
    ) -> "MissionUserListSchema":
        items = [MissionUserSchema.from_obj(mission_user=mission_user) for mission_user in mission_user_list]
        return MissionUserListSchema(items=items, limit=limit, offset=offset, total=total)


class MissionUserFilterSchema(BaseModel):
    mission_id: int | None = None
    status: OccupancyStatusEnum | None = None

    def to_obj(self) -> MissionUserFilter:
        return MissionUserFilter(mission_id=self.mission_id, status=self.status)


class MissionUserSortingSchema(BaseModel):
    field: str = "mission_id"
    type: SortType = SortType.DESC

    def to_obj(self) -> SortUserMissionObj:
        return SortUserMissionObj(field=self.field, type=self.type)
