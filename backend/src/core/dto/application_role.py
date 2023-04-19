from dataclasses import dataclass

from src.core.enum.role import ApplicationRoleEnum


@dataclass
class ApplicationRoleDTO:
    name: str


@dataclass
class ApplicationRoleCreateDTO(ApplicationRoleDTO):
    """"""


@dataclass
class UserApplicationRoleDTO:
    username: str
    application_role: ApplicationRoleEnum


@dataclass
class UserApplicationRoleUpdateDTO(UserApplicationRoleDTO):
    """"""

