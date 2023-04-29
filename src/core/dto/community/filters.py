from dataclasses import dataclass, field

from src.core.enum.community.role import CommunityRoleEnum


@dataclass
class CommunityListFilter:
    name: str | None = None
    active: bool | None = None


@dataclass
class CommunityIncludeUserFilter:
    role_list: list[CommunityRoleEnum] | None = field(default_factory=list)
