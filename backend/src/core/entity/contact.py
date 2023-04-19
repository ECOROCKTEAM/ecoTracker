from dataclasses import dataclass

from src.core.enum.contact import ContactEnum


@dataclass
class ContactType:
    id: int
    name: str


@dataclass
class Contact:
    value: str
    type: ContactEnum


@dataclass
class UserContact:
    username: str
    contact: Contact
    active: bool