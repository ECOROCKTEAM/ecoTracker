from datetime import timedelta
from enum import Enum


class SubscriptionTypeEnum(str, Enum):
    USUAL = "USUAL"
    PREMIUM = "PREMIUM"


class PeriodUnitEnum(str, Enum):
    DAY = "DAY"
    THIRTY_DAYS = "THIRTY_DAYS"