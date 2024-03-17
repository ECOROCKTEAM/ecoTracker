from typing import Annotated

from fastapi import Query
from pydantic import BaseModel

from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter


class OccupancyStatisticFilterSchema(BaseModel):
    status__in: Annotated[list[OccupancyStatusEnum] | None, Query()]

    def to_obj(self) -> OccupancyStatisticFilter:
        return OccupancyStatisticFilter(status__in=self.status__in)
