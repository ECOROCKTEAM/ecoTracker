from datetime import datetime

from pydantic import BaseModel, Field

from src.core.enum.challenges.status import OccupancyStatusEnum


class MissionUserCreateObject(BaseModel):
    """
    MissionUserCreateDTO - a model defined in OpenAPI

        mission_id: The mission_id of this MissionUserCreateDTO.
        status: The status of this MissionUserCreateDTO.
    """

    mission_id: int = Field(alias="mission_id", default=None)
    status: OccupancyStatusEnum = Field(alias="status", default=OccupancyStatusEnum.ACTIVE)


class MissionUserEntity(BaseModel):
    """
    MissionUserEntity - a model defined in OpenAPI

        id: The id of this MissionUserEntity.
        user_id: The user_id of this MissionUserEntity.
        mission_id: The mission_id of this MissionUserEntity.
        date_start: The date_start of this MissionUserEntity.
        date_close: The date_close of this MissionUserEntity.
        status: The status of this MissionUserEntity.
    """

    id: int = Field(alias="id", default=None)
    user_id: int = Field(alias="user_id", default=None)
    mission_id: int = Field(alias="mission_id", default=None)
    date_start: datetime = Field(alias="date_start", default=None)
    date_close: datetime = Field(alias="date_close", default=None)
    status: OccupancyStatusEnum = Field(alias="status", default=OccupancyStatusEnum.ACTIVE)


class MissionUserFilterObject(BaseModel):
    """
    MissionUserFilter - a model defined in OpenAPI

        mission_id: The mission_id of this MissionUserFilter.
        status: The status of this MissionUserFilter.
    """

    mission_id: int = Field(alias="mission_id", default=None)
    status: OccupancyStatusEnum = Field(alias="status", default=OccupancyStatusEnum.ACTIVE)


class MissionUserUpdateObject(BaseModel):
    """
    MissionUserUpdateDTO - a model defined in OpenAPI

        date_close: The date_close of this MissionUserUpdateDTO.
        status: The status of this MissionUserUpdateDTO.
    """

    date_close: datetime = Field(alias="date_close", default=None)
    status: OccupancyStatusEnum = Field(alias="status", default=OccupancyStatusEnum.ACTIVE)
