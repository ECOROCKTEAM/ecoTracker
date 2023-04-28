from dataclasses import dataclass

from src.core.dto.user.role import UserRoleDTO
from src.core.enum.user.role import UserRoleEnum


@dataclass
class UserRoleApplicationDTO:
    username: str
    enum: UserRoleEnum
    role: UserRoleDTO
