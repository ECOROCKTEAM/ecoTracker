from fastapi import Query
from pydantic import BaseModel

from src.core.dto.m2m.user.contact import ContactUserCreateDTO, ContactUserDTO
from src.core.enum.user.contact import ContactTypeEnum
from src.core.interfaces.repository.user.contact import UserContactFilter


class ContactFilterSchema(BaseModel):
    is_favorite: bool | None = Query(default=None)
    active: bool | None = Query(default=None)
    type: ContactTypeEnum | None = Query(default=None)

    def to_obj(self) -> UserContactFilter:
        return UserContactFilter(
            active=self.active,
            type=self.type,
            is_favorite=self.is_favorite,
        )


class ContactSchema(BaseModel):
    id: int
    user_id: str
    value: str
    type: ContactTypeEnum
    active: bool
    is_favorite: bool

    @classmethod
    def from_obj(cls, contact: ContactUserDTO) -> "ContactSchema":
        return ContactSchema(
            id=contact.id,
            user_id=contact.user_id,
            value=contact.value,
            active=contact.active,
            type=contact.type,
            is_favorite=contact.is_favorite,
        )


class ContactCreateSchema(BaseModel):
    value: str
    type: ContactTypeEnum
    active: bool

    def to_obj(self) -> ContactUserCreateDTO:
        return ContactUserCreateDTO(
            value=self.value,
            type=self.type,
            active=self.active,
            is_favorite=False,
        )


class ContactListSchema(BaseModel):
    items: list[ContactSchema]

    @classmethod
    def from_obj(cls, contact_list: list[ContactUserDTO]) -> "ContactListSchema":
        items = [ContactSchema.from_obj(contact=contact) for contact in contact_list]
        return ContactListSchema(items=items)
