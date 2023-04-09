from dataclasses import dataclass

from src.core.enum.role import RoleEnum


@dataclass
class UserCommunityRoleDTO:
    user_pointer: str
    community_pointer: str
    role: RoleEnum