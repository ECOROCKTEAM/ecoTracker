from enum import Enum


class UserRoleEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"