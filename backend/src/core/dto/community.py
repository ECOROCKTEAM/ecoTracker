from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


from src.core.enum.role import CommunityRoleEnum
from src.core.enum.community import PrivacyEnum


# TODO REMOVE DEPRICATED
@dataclass
class CreateCommunityDTO:
    name: str
    description: str
    privacy: PrivacyEnum


@dataclass
class CommunityInviteDTO:
    id: int
    community_id: str
    code: str
    expire_time: int


@dataclass
class CommunityInviteCreateDTO:
    community_id: str
    code: str
    expire_time: int


@dataclass
class CommunityInviteUpdateDTO:
    community_id: str
    code: str
    expire_time: int


@dataclass
class CommunityListFilter:
    name: Optional[str] = None
    active: Optional[bool] = None


@dataclass
class CommunityIncludeUserFilter:
    role_list: Optional[list[CommunityRoleEnum]] = field(default_factory=list)
