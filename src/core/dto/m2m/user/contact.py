from dataclasses import dataclass

from src.core.enum.user.contact import ContactTypeEnum


@dataclass
class ContactUserUpdateDTO:
    value: str | None = None
    type: ContactTypeEnum | None = None
    active: bool | None = None


@dataclass
class ContactUserDTO:
    id: int
    user_id: str
    value: str
    type: ContactTypeEnum
    active: bool
    is_favorite: bool


@dataclass
class ContactUserCreateDTO:
    value: str
    type: ContactTypeEnum
    active: bool
    is_favorite: bool
