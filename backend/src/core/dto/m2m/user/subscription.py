from dataclasses import dataclass


@dataclass
class UserSubscription:
    id: int
    username: str
    subscription_id: int
    until_date: int


@dataclass
class UserSubscriptionCreateDTO:
    username: str
    subscription_id: int
    until_date: int


@dataclass
class UserSubscriptionUpdateDTO:
    id: int
    subscription_id: int
    until_date: int
