from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query

from src.core.dto.group.group import GroupCreateDTO, GroupUpdateDTO
from src.core.dto.m2m.user.group import UserGroupUpdateDTO
from src.core.dto.mock import MockObj
from src.core.interfaces.repository.group.group import GroupFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_change_user_role import GroupChangeUserRoleUsecase
from src.core.usecases.group.group_create import GroupCreateUsecase
from src.core.usecases.group.group_delete import GroupDeleteUsecase
from src.core.usecases.group.group_get_invite_link import GroupGetInviteCodeUsecase
from src.core.usecases.group.group_join_by_code import GroupJoinByCodeUsecase
from src.core.usecases.group.group_leave import GroupLeaveUsecase
from src.core.usecases.group.group_list import GroupListUsecase
from src.core.usecases.group.group_public_add_user import GroupPublicAddUserUsecase
from src.core.usecases.group.group_update import GroupUpdateUsecase
from src.http.api.deps import get_uow, get_user

from ..models.group import Group
from ..models.group_create import GroupCreate
from ..models.group_invite_code import GroupInviteCode
from ..models.group_join_by_code import GroupJoinByCode
from ..models.group_role import GroupRole
from ..models.group_role_update import GroupRoleUpdate
from ..models.group_update import GroupUpdate

INVITE_EXPIRE_SEC = 86400 * 7


router = APIRouter()


@router.post(
    "/groups",
    responses={
        200: {"model": Group, "description": "OK"},
    },
    tags=["Group"],
    summary="Create group",
    response_model_by_alias=True,
)
async def group_create(
    group_data: GroupCreate = Body(None, description=""),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> Group:
    """Create new group"""
    uc = GroupCreateUsecase(uow=uow)
    res = await uc(user=current_user, create_obj=GroupCreateDTO(**group_data.dict()))
    return res.item


@router.delete(
    "/groups/{group_id}",
    responses={
        200: {"model": Group, "description": "OK"},
    },
    tags=["Group"],
    summary="Delete group",
    response_model_by_alias=True,
)
async def group_delete(
    group_id: int = Path(description="Group id"),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> int:
    """Delete group"""
    uc = GroupDeleteUsecase(uow=uow)
    res = await uc(user=current_user, group_id=group_id)
    return res.item


@router.get(
    "/groups",
    responses={
        200: {"model": list[Group], "description": "OK"},
        422: {"description": "User not active"},
    },
    tags=["Group"],
    summary="Group list",
    response_model_by_alias=True,
)
async def group_list(
    name: str = Query(None, description="Group name filter"),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> list[Group]:
    """Get Group list"""
    uc = GroupListUsecase(uow=uow)
    res = await uc(user=current_user, filter_obj=GroupFilter(name=name), pagination_obj=MockObj(), order_obj=MockObj())
    return res.item


@router.patch(
    "/groups/{group_id}",
    responses={
        200: {"model": Group, "description": "OK"},
    },
    tags=["Group"],
    summary="Update group",
    response_model_by_alias=True,
)
async def group_update(
    group_id: int = Path(description="group id"),
    group_data: GroupUpdate = Body(None, description=""),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> Group:
    """Update group"""
    uc = GroupUpdateUsecase(uow=uow)
    res = await uc(user=current_user, group_id=group_id, update_obj=GroupUpdateDTO(**group_data.dict()))
    return res.item


@router.get(
    "/groups/{group_id}/code",
    responses={
        200: {"model": GroupInviteCode, "description": "OK"},
    },
    tags=["Group"],
    summary="Get group code that allow joining",
    response_model_by_alias=True,
)
async def group_get_code(
    group_id: int = Path(description="group id"),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> GroupInviteCode:
    uc = GroupGetInviteCodeUsecase(uow=uow, invite_expire_sec=INVITE_EXPIRE_SEC)
    res = await uc(user=current_user, group_id=group_id)
    return res.item


@router.post(
    "/groups/{group_id}/roles",
    responses={
        200: {"model": Group, "description": "OK"},
        401: {"description": "User not active"},
    },
    tags=["Group"],
    summary="Join to public group",
    response_model_by_alias=True,
)
async def group_join(
    group_id: int = Path(description="group id"),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> GroupRole:
    uc = GroupPublicAddUserUsecase(uow=uow)
    res = await uc(user=current_user, group_id=group_id)
    return res.item


@router.post(
    "/group/join/",
    responses={
        200: {"model": Group, "description": "OK"},
        401: {"description": "User not active"},
    },
    tags=["Group"],
    summary="Join to group by code",
    response_model_by_alias=True,
)
async def group_join_by_code(
    code_data: GroupJoinByCode = Body(None, description=""),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> GroupRole:
    """Join to Group by code"""
    uc = GroupJoinByCodeUsecase(uow=uow)
    res = await uc(user=current_user, code=code_data.code)
    return res.item


@router.delete(
    "/groups/{group_id}/roles/{user_id}",
    responses={
        200: {"model": Group, "description": "OK"},
        401: {"description": "User not active"},
    },
    tags=["Group"],
    summary="Leave group",
    response_model_by_alias=True,
)
async def group_leave(
    group_id: int = Path(description="group id"),
    user_id: int = Path(description="user id"),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> bool:
    if current_user.id != user_id:
        raise HTTPException(status_code=404)
    uc = GroupLeaveUsecase(uow=uow)
    res = await uc(user=current_user, group_id=group_id)
    return res.item


@router.patch(
    "/groups/{group_id}/roles/{user_id}",
    responses={
        200: {"model": GroupRole, "description": "OK"},
        401: {"description": "User not active"},
    },
    tags=["Group"],
    summary="Update group role for specific user",
    response_model_by_alias=True,
)
async def group_role_update(
    group_id: int = Path(description="group id"),
    user_id: int = Path(description="user id"),
    group_role_data: GroupRoleUpdate = Body(None, description=""),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> GroupRole:
    uc = GroupChangeUserRoleUsecase(uow=uow)
    res = await uc(
        user=current_user,
        group_id=group_id,
        user_id=user_id,
        update_obj=UserGroupUpdateDTO(**group_role_data.dict()),
    )
    return res.item
