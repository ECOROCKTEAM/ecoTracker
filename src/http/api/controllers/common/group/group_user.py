from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_change_user_role import GroupChangeUserRoleUsecase
from src.core.usecases.group.group_get_invite_link import GroupGetInviteCodeUsecase
from src.core.usecases.group.group_join_by_code import GroupJoinByCodeUsecase
from src.core.usecases.group.group_leave import GroupLeaveUsecase
from src.core.usecases.group.group_public_add_user import GroupPublicAddUserUsecase
from src.core.usecases.group.group_user_list import GroupUserListUsecase
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.group.group_user import (
    GroupInviteLinkSchema,
    GroupUserFilterSchema,
    GroupUserLeaveSchema,
    GroupUserListSchema,
    GroupUserSchema,
    GroupUserUpdateSchema,
)

router = APIRouter()


@router.get("/list")
async def group_user_list(
    group_id: int,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
    fltr: GroupUserFilterSchema = Depends(),
) -> GroupUserListSchema:
    filter_obj = fltr.to_obj()

    uc = GroupUserListUsecase(uow=uow)
    res = await uc(user=user, group_id=group_id, filter_obj=filter_obj)
    return GroupUserListSchema.from_obj(group_user_list=res.items)


@router.get("/{group_id}/invite_link")
async def group_get_invite_link(
    group_id: int,
    invite_expire_sec: int,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
) -> GroupInviteLinkSchema:
    uc = GroupGetInviteCodeUsecase(uow=uow, invite_expire_sec=invite_expire_sec)
    res = await uc(user=user, group_id=group_id)
    return GroupInviteLinkSchema.from_obj(group_invite=res.item)


@router.post("/add")
async def public_group_add_user(
    group_id: int, uow: Annotated[IUnitOfWork, Depends(get_uow_stub)], user: Annotated[User, Depends(get_user_stub)]
) -> GroupUserSchema:
    uc = GroupPublicAddUserUsecase(uow=uow)
    res = await uc(user=user, group_id=group_id)
    return GroupUserSchema.from_obj(group_user=res.item)


@router.post("/join_by_code")
async def group_user_join_by_code(
    code: str,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
) -> GroupUserSchema:
    uc = GroupJoinByCodeUsecase(uow=uow)
    res = await uc(user=user, code=code)
    return GroupUserSchema.from_obj(group_user=res.item)


@router.patch("/role_update")
async def group_user_role_update(
    user_id: str,
    group_id: int,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
    in_obj: GroupUserUpdateSchema = Depends(),
) -> GroupUserSchema:
    obj = in_obj.to_obj()
    uc = GroupChangeUserRoleUsecase(uow=uow)
    res = await uc(user=user, user_id=user_id, group_id=group_id, update_obj=obj)
    return GroupUserSchema.from_obj(group_user=res.item)


@router.delete("/")
async def group_user_leave(
    group_id: int,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
) -> GroupUserLeaveSchema:
    uc = GroupLeaveUsecase(uow=uow)
    res = await uc(user=user, group_id=group_id)
    return GroupUserLeaveSchema.from_obj(leave_result=res.item)
