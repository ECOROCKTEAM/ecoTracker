from enum import Enum


class ApplicationRoleEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"