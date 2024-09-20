from typing import Annotated

from fastapi import Query
from pydantic import BaseModel

from src.core.entity.occupancy import OccupancyCategory
from src.core.enum.language import LanguageEnum
from src.core.interfaces.repository.challenges.occupancy import OccupancyFilter


class OccupancySchema(BaseModel):
    id: int
    name: str
    language: LanguageEnum


class OccupancyListSchema(BaseModel):
    items: list[OccupancySchema]

    @classmethod
    def from_obj(cls, occupancy_list: list[OccupancyCategory]) -> "OccupancyListSchema":
        items = [
            OccupancySchema(id=occupancy.id, name=occupancy.name, language=occupancy.language)
            for occupancy in occupancy_list
        ]
        return OccupancyListSchema(items=items)


class OccupancyFilterSchema(BaseModel):
    id__in: Annotated[list[int] | None, Query()]

    def to_obj(self) -> OccupancyFilter:
        return OccupancyFilter(id__in=self.id__in)
