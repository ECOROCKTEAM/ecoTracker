from dataclasses import dataclass
from typing import Generic, TypeVar

from src.core.enum.utils import SortType

T = TypeVar("T")


@dataclass
class IterableObj:
    limit: int | None = None
    offset: int = 0


@dataclass
class SortObj:
    field: str = "id"
    type: SortType = SortType.DESC


@dataclass
class SortUserTaskObj(SortObj):
    field: str = "task_id"


@dataclass
class Pagination(Generic[T]):
    items: T
    limit: int | None
    offset: int
    total: int
