from dataclasses import dataclass, field
from typing import Optional

from src.core.enum.community.role import CommunityRoleEnum

@dataclass
class CommunityListFilter:
    name: Optional[str] = None
    active: Optional[bool] = None


@dataclass
class CommunityIncludeUserFilter:
    role_list: Optional[list[CommunityRoleEnum]] = field(default_factory=list)