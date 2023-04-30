from src.core.enum.base.translation import TranslationEnum


class OccupancyStatusEnum(str, TranslationEnum):
    ACTIVE = "ACTIVE"
    FINISH = "FINISH"
    REJECT = "REJECT"
    OVERDUE = "OVERDUE"
