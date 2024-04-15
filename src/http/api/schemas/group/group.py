from pydantic import BaseModel

from src.core.dto.group.group import GroupCreateDTO, GroupUpdateDTO
from src.core.entity.group import Group
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.utils import SortType
from src.core.interfaces.repository.group.group import GroupFilter, SortingGroupObj


class GroupUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    active: bool | None = None
    privacy: GroupPrivacyEnum | None = None

    def to_obj(self) -> GroupUpdateDTO:
        return GroupUpdateDTO(name=self.name, description=self.description, active=self.active, privacy=self.privacy)


class GroupDeleteSchema(BaseModel):
    group_id: int


class GroupListFilterSchema(BaseModel):
    active: bool | None = None
    user_id: str | None = None

    def to_obj(self) -> GroupFilter:
        return GroupFilter(active=self.active, user_id=self.user_id)


class GroupListSortingSchema(BaseModel):
    field: str = "id"
    type: SortType = SortType.DESC

    def to_obj(self) -> SortingGroupObj:
        return SortingGroupObj(field=self.field, type=self.type)


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


class GroupListSchema(BaseModel):
    item: list[GroupSchema]
    limit: int | None
    offset: int
    total: int

    @classmethod
    def from_obj(cls, group_list: list[Group], limit: int | None, offset: int, total: int) -> "GroupListSchema":
        items = [GroupSchema.from_obj(group=group) for group in group_list]
        return GroupListSchema(item=items, limit=limit, offset=offset, total=total)


class GroupCreateSchema(BaseModel):
    name: str
    privacy: GroupPrivacyEnum
    description: str
    active: bool

    def to_obj(self) -> GroupCreateDTO:
        return GroupCreateDTO(name=self.name, privacy=self.privacy, description=self.description, active=self.active)
