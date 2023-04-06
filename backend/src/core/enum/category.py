from enum import Enum


class OccupancyStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    FINISH = "FINISH"
    REJECT = "REJECT"
    OVERDUE = "OVERDUE"
