from dataclasses import dataclass

from src.core.enum.group.role import GroupRoleEnum


@dataclass
class UserGroupDTO:
    user_id: str
    group_id: int
    role: GroupRoleEnum


@dataclass
class UserGroupUpdateDTO:
    role: GroupRoleEnum


@dataclass
class UserGroupCreateDTO:
    user_id: str
    group_id: int
    role: GroupRoleEnum
