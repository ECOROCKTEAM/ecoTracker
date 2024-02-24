from dataclasses import dataclass

from src.core.enum.utils import SortType


@dataclass
class IterableObj:
    limit: int | None = None
    offset: int = 0


@dataclass
class SortObj:
    field: str = "id"
    type: SortType = SortType.DESC
