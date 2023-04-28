from dataclasses import dataclass
from typing import Optional

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
    subscription: Subscription
    role: UserRoleDTO


@dataclass
class UserUpdateDTO:
    user_id: str  # username reference
    username: Optional[str] = None
    password: Optional[str] = None
    active: Optional[bool] = None
    subscription: Optional[Subscription] = None
    role: Optional[UserRoleDTO] = None
