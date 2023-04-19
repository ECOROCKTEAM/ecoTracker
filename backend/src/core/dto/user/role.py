from dataclasses import dataclass
from src.core.enum.user.role import UserRoleEnum

@dataclass
class UserRoleDTO:
    enum: UserRoleEnum


@dataclass
class UserRoleCreateDTO:
    enum: UserRoleEnum
