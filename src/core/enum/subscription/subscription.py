from src.core.enum.base.translation import TranslationEnum


class SubscriptionTypeEnum(str, TranslationEnum):
    USUAL = "USUAL"
    PREMIUM = "PREMIUM"


class PeriodUnitEnum(str, TranslationEnum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
