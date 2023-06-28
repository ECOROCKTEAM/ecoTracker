from pydantic import BaseModel, Field

from src.core.enum.language import LanguageEnum


class OccupancyCategorySchema(BaseModel):
    """
    OccupancyCategorySchema - a model defined in OpenAPI

        id: The id of this OccupancyCategorySchema .
        name: The name of this OccupancyCategorySchema .
        language: The language of this OccupancyCategorySchema .
    """

    id: int = Field(alias="id", default=None)
    name: str = Field(alias="name", default=None)
    language: LanguageEnum = Field(alias="language")
