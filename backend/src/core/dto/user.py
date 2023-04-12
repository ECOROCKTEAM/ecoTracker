from typing import List

from dataclasses import dataclass
<<<<<<< HEAD
from src.core.enum.contact import ContactEnum
from src.core.dto.base import  TypeDTO
=======
from src.core.dto.base import TypeDTO
>>>>>>> fabfd75ad109dc623b1541a22c5297633fe648d0


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
<<<<<<< HEAD


@dataclass
class CreateUserDTO:
    username: str
    password: str
    contact: str
    contact_type: ContactEnum
=======
>>>>>>> fabfd75ad109dc623b1541a22c5297633fe648d0
