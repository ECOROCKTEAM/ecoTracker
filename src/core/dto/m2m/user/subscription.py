from dataclasses import dataclass


@dataclass
class UserSubscription:
    id: int
    user_id: str
    subscription_id: int
    until_date: int


@dataclass
class UserSubscriptionCreateDTO:
    user_id: str
    subscription_id: int
    until_date: int


@dataclass
class UserSubscriptionUpdateDTO:
    subscription_id: int
    until_date: int
