from dataclasses import dataclass

from src.core.dto.community.role import CommunityRoleDTO


@dataclass
class UserCommunityDTO:
    id: int
    user_id: str
    community_id: str
    role: CommunityRoleDTO

@dataclass
class UserCommunityUpdateDTO:
    id: int
    user_id: str
    community_id: str
    role_id: int

@dataclass
class UserCommunityCreateDTO:
    user_id: str
    community_id: str
    role_id: int
