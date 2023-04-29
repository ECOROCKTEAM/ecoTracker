from dataclasses import dataclass

from src.core.entity.subscription import Subscription
from src.core.dto.user.role import UserRoleDTO


@dataclass
class User:
    """User entity"""

    username: str
    password: str
    active: bool
    subscription: Subscription
    role: UserRoleDTO

    @property
    def is_premium(self) -> bool:
        # TODO implement!
        raise NotImplementedError


@dataclass
class UserCreateDTO:
    username: str
    password: str
    active: bool
    role: UserRoleDTO


@dataclass
class UserUpdateDTO:
    user_id: str  # username reference
    username: str | None = None
    password: str | None = None
    active: bool | None = None
    role: UserRoleDTO | None = None

