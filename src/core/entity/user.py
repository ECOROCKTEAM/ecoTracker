from dataclasses import dataclass

from src.core.entity.subscription import Subscription
from src.core.enum.language import LanguageEnum


@dataclass
class User:
    """User entity"""

    id: int
    username: str
    password: str
    active: bool
    subscription: Subscription
    language: LanguageEnum

    @property
    def is_premium(self) -> bool:
        # TODO implement!
        raise NotImplementedError


@dataclass
class UserCreateDTO:
    username: str
    password: str
    active: bool
    language: LanguageEnum


@dataclass
class UserUpdateDTO:
    user_id: int  # username reference
    username: str | None = None
    password: str | None = None
    active: bool | None = None
    language: LanguageEnum | None = None
