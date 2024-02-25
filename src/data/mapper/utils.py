from sqlalchemy import Select, asc, desc

from src.core.dto.utils import IterableObj, SortObj
from src.core.enum.utils import SortType

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
