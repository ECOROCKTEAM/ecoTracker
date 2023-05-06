from dataclasses import dataclass
from src.core.enum.community.role import CommunityRoleEnum


@dataclass
class UserCommunityDTO:
    user_id: int
    community_id: int
    role: CommunityRoleEnum


@dataclass
class UserCommunityUpdateDTO:
    role: CommunityRoleEnum


@dataclass
class UserCommunityCreateDTO:
    user_id: int
    community_id: int
    role: CommunityRoleEnum
