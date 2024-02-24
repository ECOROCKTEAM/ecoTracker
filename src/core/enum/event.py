from enum import IntEnum, unique


@unique
class EventTypeEnum(IntEnum):
    NEW_ANNOUNCMENT = 1  # some news from admin
    NEW_MISSION = 2
    NEW_TASK = 3
