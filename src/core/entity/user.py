from dataclasses import dataclass

from src.core.entity.subscription import Subscription
from src.core.enum.language import LanguageEnum


@dataclass
class User:
    """User entity"""

    id: str
    username: str
    password: str
    active: bool
    subscription: Subscription
    language: LanguageEnum

    @property
    def is_premium(self) -> bool:
        # TODO implement!
        return True


@dataclass
class UserCreateDTO:
    id: str
    username: str
    password: str
    active: bool
    language: LanguageEnum


@dataclass
class UserUpdateDTO:
    user_id: str  # username reference
    username: str | None = None
    password: str | None = None
    active: bool | None = None
    language: LanguageEnum | None = None
