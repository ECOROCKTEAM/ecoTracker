from enum import Enum, EnumMeta

# BASE HREF


class UsersT(Enum):
    USER__ACTIVE = 1
    USER__NOT_ACTIVE = 2


class CategoryT(Enum):
    CATEGORY__OK_TRANSLATE = 1
    CATEGORY__BAD_TRANSLATE = 2


class MissionT(Enum):
    MISSION__ACTIVE = 1
    MISSION__NOT_ACTIVE = 2


# USECASE PREPARE


class MissionGetUsecaseT(Enum):
    OK = dict(user=UsersT.USER__ACTIVE, mission=MissionT.MISSION__ACTIVE)
    MISSION_NOT_ACTIVE = dict(user=UsersT.USER__ACTIVE, mission=MissionT.MISSION__NOT_ACTIVE)
