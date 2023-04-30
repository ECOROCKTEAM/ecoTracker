from dataclasses import dataclass

from src.core.dto.mock import MockObj


@dataclass
class UserTaskFilter:
    filter_obj: MockObj | None = None
    sorting_obj: MockObj | None = None
    order_obj: MockObj | None = None
