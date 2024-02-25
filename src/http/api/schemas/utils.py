from typing import TypeVar

from fastapi import Query
from pydantic import BaseModel

from src.core.dto.utils import IterableObj, SortObj
from src.core.enum.utils import SortType

T = TypeVar("T")


class IterableSchema(BaseModel):
    limit: int | None = Query(default=None)
    offset: int = Query(default=0)

    def to_obj(self) -> IterableObj:
        return IterableObj(
            limit=self.limit,
            offset=self.offset,
        )


class SortSchema(BaseModel):
    sort_field: str = Query(default="id")
    sort_type: SortType = Query(default=SortType.DESC)

    def to_obj(self) -> SortObj:
        return SortObj(
            field=self.sort_field,
            type=self.sort_type,
        )
