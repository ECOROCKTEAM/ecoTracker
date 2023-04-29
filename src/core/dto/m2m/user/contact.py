from dataclasses import dataclass
from typing import Optional

from src.core.dto.user.contact import ContactDTO, ContactTypeDTO


@dataclass
class ContactUser:
    id: int
    username: str
    contact: ContactDTO
    active: bool


@dataclass
class ContactUserUpdateDTO:
    contact_id: int
    contact: Optional[ContactDTO] = None
    active: Optional[bool] = None


@dataclass
class ContactUserDTO:
    id: int
    username: str
    contact: ContactDTO
    type: ContactTypeDTO
    active: bool


@dataclass 
class ContactUserCreateDTO:
    username: str
    value: str
    type: ContactTypeDTO
    active: bool = True
