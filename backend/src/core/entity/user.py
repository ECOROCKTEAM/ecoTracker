from dataclasses import dataclass

from src.core.enum.role import ApplicationRoleEnum
from src.core.entity.subscription import Subscription


@dataclass
class User:
    """User entity"""

    username: str
    password: str
    active: bool
    subscription: Subscription
    application_role: ApplicationRoleEnum

    @property
    def is_premium(self) -> bool:
        # TODO implement!
        raise NotImplementedError