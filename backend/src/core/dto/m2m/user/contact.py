from dataclasses import dataclass
from typing import Optional

from src.core.dto.user.contact import ContactDTO


@dataclass
class ContactUser:
    id: int
    username: str
    contact: ContactDTO
    active: bool


@dataclass
class ContactUserUpdateDTO:
    id: int
    contact: Optional[ContactDTO] = None
    active: Optional[bool] = None


@dataclass
class ContactUserDTO:
    username: str
    contact: ContactDTO
    active: bool