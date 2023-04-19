from dataclasses import dataclass


@dataclass
class SubscriptionTypeConstrainDTO:
    type_id: int
    constraint_id: int


@dataclass
class SubscriptionTypeConstrainCreateDTO:
    type_id: int
    constraint_id: int
