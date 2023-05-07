from dataclasses import dataclass
from src.core.enum.community.role import CommunityRoleEnum


@dataclass
class UserCommunityDTO:
    id: int
    user_id: int
    community_id: str
    role: CommunityRoleEnum


@dataclass
class UserCommunityUpdateDTO:
    id: int
    user_id: int
    community_id: str
    role: CommunityRoleEnum


@dataclass
class UserCommunityCreateDTO:
    user_id: int
    community_id: str
    role: CommunityRoleEnum
