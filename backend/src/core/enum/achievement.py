from enum import Enum


class AchievementStatusEnum(str, Enum):
    RECEIVED = "RECEIVED"
    UNCOMPLETED = "UNCOMPLETED"


class AchivmentRelatedWithEnum(str, Enum):
    TASK = "TASK"
    SUBSCRIPTION = "SUBSCRIPTION"
    MISSION = "MISSION"
    NUMBER_OF_USERS = "NUMBER_OF_USERS"
