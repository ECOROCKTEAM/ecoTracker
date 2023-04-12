from dataclasses import dataclass

from src.core.entity.subscription import Subscription
from src.core.enum.role import ApplicationRoleEnum


@dataclass
class User:
    """User entity"""

    id: int
    username: str
    password: str
    active: bool
    subscription: Subscription
    application_role: ApplicationRoleEnum

    @property
    def is_premium(self) -> bool:
        # TODO implement!
        raise NotImplementedError