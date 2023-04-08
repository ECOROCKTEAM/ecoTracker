from dataclasses import dataclass

from src.core.entity.subscription import Subscription


@dataclass
class User:
    """User entity"""

    username: str
    password: str
    active: bool
    subscription: Subscription
