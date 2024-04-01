from pydantic import BaseModel

from src.core.dto.group.group import GroupCreateDTO
from src.core.entity.group import Group
from src.core.enum.group.privacy import GroupPrivacyEnum


class GroupSchema(BaseModel):
    id: int
    name: str
    description: str
    active: bool
    privacy: GroupPrivacyEnum

    @classmethod
    def from_obj(cls, group: Group) -> "GroupSchema":
        return GroupSchema(
            id=group.id,
            name=group.name,
            description=group.description,
            active=group.active,
            privacy=group.privacy,
        )


class GroupCreateSchema(BaseModel):
    name: str
    privacy: GroupPrivacyEnum
    description: str
    active: bool

    def to_obj(self) -> GroupCreateDTO:
        return GroupCreateDTO(name=self.name, privacy=self.privacy, description=self.description, active=self.active)
