from dataclasses import dataclass
from src.core.enum.subscription.subscription import SubscriptionPeriodUnitEnum


@dataclass
class SubscriptionPeriodCreateDTO:
    value: int
    unit: SubscriptionPeriodUnitEnum


@dataclass
class SubscriptionPeriodDTO:
    id: int
    value: int
    unit: SubscriptionPeriodUnitEnum
