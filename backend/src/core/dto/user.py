from typing import List
from dataclasses import dataclass

from src.core.enum.role import ApplicationRoleEnum
from src.core.enum.subscription import SubscriptionTypeEnum
from src.core.enum.contact import ContactEnum
from src.core.dto.base import  TypeDTO


@dataclass
class UserContactTypeDTO(TypeDTO):
    """"""


@dataclass
class UserContactDTO:
    value: str
    active: bool
    type: UserContactTypeDTO


@dataclass
class UserContactListDTO:
    contacts: List[UserContactDTO]

    def __getattr__(self, request_type: str):
        tmp = None
        for contact in self.contacts:
            if contact.type.name == request_type:
                tmp = contact
                break
        else:
            raise Exception("Not found")
        return tmp


@dataclass
class UserDTO:
    username: str
    password: str


@dataclass
class UserUpdateDTO(UserDTO):
    """"""


@dataclass
class UserContactDTO(UserDTO):
    contact: str
    type: ContactEnum


@dataclass
class UserCreateDTO:
    username: str
    password: str
    contact: str
    type: ContactEnum
    subscription: SubscriptionTypeEnum
    application_role: ApplicationRoleEnum


