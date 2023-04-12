from dataclasses import dataclass

from src.core.enum.role import CommunityRoleEnum


@dataclass
class UserCommunityDTO:
    id: int
    user_id: str
    community_id: str
    role: CommunityRoleEnum


@dataclass
class UserCommunityCreateDTO:
    id: int
    user_id: str
    community_id: str
    role: CommunityRoleEnum = CommunityRoleEnum.USER
