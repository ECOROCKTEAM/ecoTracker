from enum import Enum


class CommunityRoleEnum(str, Enum):
    SUPERUSER = "SUPERUSER"
    ADMIN = "ADMIN"
    USER = "USER"
    BLOCKED = "BLOCKED"
