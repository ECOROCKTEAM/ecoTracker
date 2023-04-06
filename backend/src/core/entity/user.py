from dataclasses import dataclass

from backend.src.core.entity.subscription import Subscription
from backend.src.core.enum.community import RoleEnum


@dataclass
class User:
    """User entity"""

    username: str
    password: str
    active: bool
    subscription: Subscription


@dataclass
class UserCommunityRoleDTO:
    user_pointer: str
    community_pointer: str
    role: RoleEnum
