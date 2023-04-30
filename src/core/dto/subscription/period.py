from dataclasses import dataclass
from src.core.enum.subscription.subscription import PeriodUnitEnum


@dataclass
class SubscriptionPeriodCreateDTO:
    value: int
    unit: PeriodUnitEnum



@dataclass
class SubscriptionPeriodDTO:
    id: int
    value: int
    unit: PeriodUnitEnum
