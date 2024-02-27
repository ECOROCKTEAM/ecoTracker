from collections.abc import Sequence
from typing import TypeVar

from sqlalchemy import Select, asc, desc

from src.core.dto.utils import IterableObj, Pagination, SortObj
from src.core.enum.utils import SortType

T = TypeVar("T")

_SQLALCHEMY_SORT_TYPE_MAP = {
    SortType.ASC: asc,
    SortType.DESC: desc,
}


def apply_iterable(stmt: Select, iterable_obj: IterableObj) -> Select:
    if iterable_obj.limit is not None:
        stmt = stmt.limit(iterable_obj.limit)
    stmt = stmt.offset(iterable_obj.offset)
    return stmt


def apply_sorting(stmt: Select, sorting_obj: SortObj) -> Select:
    operator = _SQLALCHEMY_SORT_TYPE_MAP[sorting_obj.type]
    stmt = stmt.order_by(operator(sorting_obj.field))
    return stmt


def recive_total(seq: Sequence, total_idx: int) -> int:
    if len(seq) == 0:
        return 0
    return seq[total_idx]


def build_pagination(items: list[T], iterable_obj: IterableObj, total: int) -> Pagination[list[T]]:
    return Pagination(items=items, limit=iterable_obj.limit, offset=iterable_obj.offset, total=total)
