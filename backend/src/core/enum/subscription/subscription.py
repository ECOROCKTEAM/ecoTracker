from enum import Enum


class SubscriptionTypeEnum(str, Enum):
    USUAL = "USUAL"
    PREMIUM = "PREMIUM"


class PeriodUnitEnum(str, Enum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"