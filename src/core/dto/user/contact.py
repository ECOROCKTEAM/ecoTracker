from dataclasses import dataclass

from src.core.enum.user.contact import ContactTypeEnum


@dataclass
class ContactDTO:
    id: int
    value: str
    type: ContactTypeEnum


@dataclass
class ContactCreateDTO:
    value: str
    type: ContactTypeEnum


@dataclass
class ContactUpdateDTO:
    contact_id: int
    value: str | None = None
    active: bool | None = None
