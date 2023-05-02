from dataclasses import dataclass

from src.core.entity.subscription import Subscription


@dataclass
class User:
    """User entity"""

    username: str
    password: str
    active: bool
    subscription: Subscription

    @property
    def is_premium(self) -> bool:
        # TODO implement!
        raise NotImplementedError


@dataclass
class UserCreateDTO:
    username: str
    password: str
    active: bool


@dataclass
class UserUpdateDTO:
    user_id: str  # username reference
    username: str | None = None
    password: str | None = None
    active: bool | None = None
