from pydantic import BaseModel

from src.core.entity.occupancy import OccupancyCategory


class OccupancySchema(BaseModel):
    occupancy: OccupancyCategory


class OccupancyListSchema(BaseModel):
    items: list[OccupancySchema]

    @classmethod
    def from_obj(cls, occupancy_list: list[OccupancyCategory]) -> "OccupancyListSchema":
        items = [OccupancySchema(occupancy=occupancy) for occupancy in occupancy_list]
        return OccupancyListSchema(items=items)
