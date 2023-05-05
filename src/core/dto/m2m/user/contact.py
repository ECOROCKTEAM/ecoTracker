from dataclasses import dataclass

from src.core.dto.user.contact import ContactDTO
from src.core.enum.user.contact import ContactTypeEnum


@dataclass
class ContactUserUpdateDTO:
    contact_id: int
    contact: ContactDTO | None = None
    active: bool | None = None


@dataclass
class ContactUserDTO:
    id: int
    username: str
    contact: ContactDTO
    active: bool


@dataclass
class ContactUserCreateDTO:
    username: str
    value: str
    type: ContactTypeEnum
    active: bool = True
