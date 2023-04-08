from enum import Enum


class RoleEnum(str, Enum):
    SUPERUSER = "SUPERUSER"
    ADMIN = "ADMIN"
    USER = "USER"
