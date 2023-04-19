from dataclasses import dataclass
from datetime import datetime

from src.core.enum.role import ApplicationRoleEnum
from src.core.entity.subscription import Subscription
from src.core.enum.application.role import ApplicationRoleEnum


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
<<<<<<< HEAD
        raise NotImplementedError
=======
        raise NotImplementedError
    

@dataclass
class UserSubscription:

    username: str
    subscription_id: int
    cancelled: bool
    until_date: datetime


@dataclass
class UserTask:
    username: str
    task_id: int
    occupancy_status_id: int


@dataclass
class UserRoleApplication:
    username: str
    role: ApplicationRoleEnum
>>>>>>> origin/develop
