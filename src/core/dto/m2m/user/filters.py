from dataclasses import dataclass
from typing import Optional

from src.core.dto.mock import MockObj


@dataclass
class UserTaskFilter:
    filter_obj: Optional[MockObj] = None
    sorting_obj: Optional[MockObj] = None
    order_obj: Optional[MockObj] = None