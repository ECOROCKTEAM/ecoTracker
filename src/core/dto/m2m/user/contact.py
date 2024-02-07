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
    user_id: str
    contact: ContactDTO
    active: bool
    is_favorite: bool


@dataclass
class ContactUserCreateDTO:
    user_id: str
    value: str
    type: ContactTypeEnum
    active: bool = True
    is_favorite: bool = False
