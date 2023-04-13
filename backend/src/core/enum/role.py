from enum import Enum


class ApplicationRoleEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class RoleEnum(str, Enum):
    SUPERUSER = "SUPERUSER"
    ADMIN = "ADMIN"
    USER = "USER"
