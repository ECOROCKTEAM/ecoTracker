from pydantic import BaseModel, Field

from src.core.enum.language import LanguageEnum


class MissionFilterQueryParams:
    def __init__(self, active: bool | None = True) -> None:
        self.active = active


class MissionEntity(BaseModel):
    """
    MissionEntity - a model defined in OpenAPI

        id: The id of this MissionEntity.
        name: The name of this MissionEntity.
        active: The active of this MissionEntity.
        description: The description of this MissionEntity.
        instruction: The instruction of this MissionEntity.
        category_id: The category_id of this MissionEntity.
        language: The language of this MissionEntity.
    """

    id: int = Field(alias="id", default=None)
    name: str = Field(alias="name", default=None)
    active: bool = Field(alias="active", default=True)
    description: str = Field(alias="description", default=None)
    instruction: str = Field(alias="instruction", default=None)
    category_id: int = Field(alias="category_id", default=None)
    language: LanguageEnum = Field(alias="language", default=None)
