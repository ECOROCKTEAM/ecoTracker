from datetime import date, datetime

from pydantic import BaseModel, Field

from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum


class TaskFilterObject(BaseModel):
    active: bool = Field(alias="active", default=None)
    category_id: int = Field(alias="category_id", default=None)


class TaskUserPlanFilterObject(BaseModel):
    task_active: bool = Field(alias="task_active", default=True)


class TaskUserFilterObject(BaseModel):
    task_id: int = Field(alias="task_id", default=None)
    task_active: bool = Field(alias="task_active", default=True)
    status: OccupancyStatusEnum = Field(alias="status", default=OccupancyStatusEnum.ACTIVE)


class Task(BaseModel):
    """
    id: The id of this TaskEntity [Optional.
    score: The score of this TaskEntity [Optional.
    category_id: The category_id of this TaskEntity [Optional.
    name: The name of this TaskEntity [Optional.
    active: The active of this TaskEntity [Optional.
    description: The description of this TaskEntity [Optional.
    language: The language of this TaskEntity [Optional.
    """

    id: int = Field(alias="id", default=None)
    score: int = Field(alias="score", default=None)
    category_id: int = Field(alias="category_id", default=None)
    name: str = Field(alias="name", default=None)
    active: bool = Field(alias="active", default=None)
    description: str = Field(alias="description", default=None)
    language: LanguageEnum = Field(alias="language", default=None)


class TaskUserEntity(BaseModel):
    """
    user_id: The user_id of this TaskUserEntity [Optional.
    task_id: The task_id of this TaskUserEntity [Optional.
    date_start: The date_start of this TaskUserEntity [Optional.
    date_close: The date_close of this TaskUserEntity [Optional.
    status: The status of this TaskUserEntity [Optional.
    """

    user_id: int = Field(alias="user_id", default=None)
    task_id: int = Field(alias="task_id", default=None)
    date_start: date = Field(alias="date_start", default=None)
    date_close: datetime = Field(alias="date_close", default=None)
    status: OccupancyStatusEnum = Field(alias="status", default=None)


class TaskUserPlanEntity(BaseModel):
    """
    user_id: The user_id of this TaskUserPlanEntity [Optional.
    task_id: The task_id of this TaskUserPlanEntity [Optional.
    """

    user_id: int = Field(alias="user_id", default=None)
    task_id: int = Field(alias="task_id", default=None)
