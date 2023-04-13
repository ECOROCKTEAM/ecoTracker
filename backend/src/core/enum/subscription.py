from datetime import timedelta
from enum import Enum


class SubscriptionTypeEnum(str, Enum):
    USUAL = "USUAL"
    PREMIUM = "PREMIUM"


class PeriodUnitEnum(str, Enum):
    DAY = timedelta(days=1)
    THIRTY_DAYS = timedelta(days=30)