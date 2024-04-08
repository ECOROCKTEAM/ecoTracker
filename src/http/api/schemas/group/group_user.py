from datetime import datetime
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel

from src.core.dto.group.invite import GroupInviteDTO
from src.core.dto.m2m.user.group import UserGroupDTO, UserGroupUpdateDTO
from src.core.enum.group.role import GroupRoleEnum
from src.core.interfaces.repository.group.group import GroupUserFilter


class GroupUserFilterSchema(BaseModel):
    role__in: Annotated[list[GroupRoleEnum] | None, Query()]
    user_id__in: Annotated[list[str] | None, Query()]

    def to_obj(self) -> GroupUserFilter:
        return GroupUserFilter(role__in=self.role__in, user_id__in=self.user_id__in)


class GroupUserLeaveSchema(BaseModel):
    operation_result: bool

    @classmethod
    def from_obj(cls, leave_result: bool) -> "GroupUserLeaveSchema":
        return GroupUserLeaveSchema(operation_result=leave_result)


class GroupUserUpdateSchema(BaseModel):
    role: GroupRoleEnum

    def to_obj(self) -> UserGroupUpdateDTO:
        return UserGroupUpdateDTO(role=self.role)


class GroupUserSchema(BaseModel):
    user_id: str
    group_id: int
    role: GroupRoleEnum

    @classmethod
    def from_obj(cls, group_user: UserGroupDTO) -> "GroupUserSchema":
        return GroupUserSchema(user_id=group_user.user_id, group_id=group_user.group_id, role=group_user.role)


class GroupUserListSchema(BaseModel):
    items: list[GroupUserSchema]

    @classmethod
    def from_obj(cls, group_user_list: list[UserGroupDTO]) -> "GroupUserListSchema":
        items = [GroupUserSchema.from_obj(group_user=group_user) for group_user in group_user_list]
        return GroupUserListSchema(items=items)


class GroupInviteLinkSchema(BaseModel):
    group_id: int
    code: str | None
    expire_time: datetime | None

    @classmethod
    def from_obj(cls, group_invite: GroupInviteDTO) -> "GroupInviteLinkSchema":
        return GroupInviteLinkSchema(
            group_id=group_invite.group_id, code=group_invite.code, expire_time=group_invite.expire_time
        )
