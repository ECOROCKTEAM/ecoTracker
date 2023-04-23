from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class UserSubscriptionDTO:
    id: int
    username: str
    subscription_id: int
    cancelled: bool
    until_date: int


@dataclass
class UserSubscriptionCreateDTO:
    username: str
    subscription_id: int
    until_date: datetime
    cancelled: bool = True


@dataclass
class UserSubscriptionUpdateDTO:
    id: int
    cancelled: bool = True


@dataclass
class UserSubscriptionUpdateDTO:
    id: int
    subscription_id: Optional[int] = None
    cancelled: Optional[bool] = True
    until_date: Optional[datetime] = None
