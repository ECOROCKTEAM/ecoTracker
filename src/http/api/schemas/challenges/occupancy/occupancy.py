from fastapi import Query
from pydantic import BaseModel

from src.core.entity.occupancy import OccupancyCategory
from src.core.interfaces.repository.challenges.occupancy import OccupancyFilter


class OccupancySchema(BaseModel):
    occupancy: OccupancyCategory


class OccupancyListSchema(BaseModel):
    items: list[OccupancySchema]

    @classmethod
    def from_obj(cls, occupancy_list: list[OccupancyCategory]) -> "OccupancyListSchema":
        items = [OccupancySchema(occupancy=occupancy) for occupancy in occupancy_list]
        return OccupancyListSchema(items=items)


class OccupancyFilterSchema(BaseModel):
    items: list[int] | None = Query(default=None)

    def to_obj(self) -> OccupancyFilter:
        return OccupancyFilter(id_in=self.items)
