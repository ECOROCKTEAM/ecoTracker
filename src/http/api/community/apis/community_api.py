from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query

from src.core.dto.community.community import CommunityCreateDTO, CommunityUpdateDTO
from src.core.dto.m2m.user.community import UserCommunityUpdateDTO
from src.core.dto.mock import MockObj
from src.core.interfaces.repository.community.community import CommunityFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.community.community_change_user_role import (
    CommunityChangeUserRoleUsecase,
)
from src.core.usecases.community.community_create import CommunityCreateUsecase
from src.core.usecases.community.community_delete import CommunityDeleteUsecase
from src.core.usecases.community.community_get_invite_link import (
    CommunityGetInviteCodeUsecase,
)
from src.core.usecases.community.community_join_by_code import (
    CommunityJoinByCodeUsecase,
)
from src.core.usecases.community.community_leave import CommunityLeaveUsecase
from src.core.usecases.community.community_list import CommunityListUsecase
from src.core.usecases.community.community_public_add_user import (
    CommunityPublicAddUserUsecase,
)
from src.core.usecases.community.community_update import CommunityUpdateUsecase
from src.http.api.deps import get_uow, get_user

from ..models.community import Community
from ..models.community_create import CommunityCreate
from ..models.community_invite_code import CommunityInviteCode
from ..models.community_join_by_code import CommunityJoinByCode
from ..models.community_role import CommunityRole
from ..models.community_role_update import CommunityRoleUpdate
from ..models.community_update import CommunityUpdate

INVITE_EXPIRE_SEC = 86400 * 7


router = APIRouter()


@router.post(
    "/communities",
    responses={
        200: {"model": Community, "description": "OK"},
    },
    tags=["Community"],
    summary="Create community",
    response_model_by_alias=True,
)
async def community_create(
    community_data: CommunityCreate = Body(None, description=""),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> Community:
    """Create new community"""
    uc = CommunityCreateUsecase(uow=uow)
    res = await uc(user=current_user, create_obj=CommunityCreateDTO(**community_data.dict()))
    return res.item


@router.delete(
    "/communities/{community_id}",
    responses={
        200: {"model": Community, "description": "OK"},
    },
    tags=["Community"],
    summary="Delete community",
    response_model_by_alias=True,
)
async def community_delete(
    community_id: int = Path(description="community id"),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> int:
    """Delete community"""
    uc = CommunityDeleteUsecase(uow=uow)
    res = await uc(user=current_user, community_id=community_id)
    return res.item


@router.get(
    "/communities",
    responses={
        200: {"model": list[Community], "description": "OK"},
        422: {"description": "User not active"},
    },
    tags=["Community"],
    summary="Community list",
    response_model_by_alias=True,
)
async def community_list(
    name: str = Query(None, description="Community name filter"),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> list[Community]:
    """Get community list"""
    uc = CommunityListUsecase(uow=uow)
    res = await uc(
        user=current_user, filter_obj=CommunityFilter(name=name), pagination_obj=MockObj(), order_obj=MockObj()
    )
    return res.item


@router.patch(
    "/communities/{community_id}",
    responses={
        200: {"model": Community, "description": "OK"},
    },
    tags=["Community"],
    summary="Update community",
    response_model_by_alias=True,
)
async def community_update(
    community_id: int = Path(description="community id"),
    community_data: CommunityUpdate = Body(None, description=""),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> Community:
    """Update community"""
    uc = CommunityUpdateUsecase(uow=uow)
    res = await uc(user=current_user, community_id=community_id, update_obj=CommunityUpdateDTO(**community_data.dict()))
    return res.item


@router.get(
    "/communities/{community_id}/code",
    responses={
        200: {"model": CommunityInviteCode, "description": "OK"},
    },
    tags=["Community"],
    summary="Get community code that allow joining",
    response_model_by_alias=True,
)
async def community_get_code(
    community_id: int = Path(description="community id"),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> CommunityInviteCode:
    uc = CommunityGetInviteCodeUsecase(uow=uow, invite_expire_sec=INVITE_EXPIRE_SEC)
    res = await uc(user=current_user, community_id=community_id)
    return res.item


@router.post(
    "/communities/{community_id}/roles",
    responses={
        200: {"model": Community, "description": "OK"},
        401: {"description": "User not active"},
    },
    tags=["Community"],
    summary="Join to public community",
    response_model_by_alias=True,
)
async def community_join(
    community_id: int = Path(description="community id"),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> CommunityRole:
    uc = CommunityPublicAddUserUsecase(uow=uow)
    res = await uc(user=current_user, community_id=community_id)
    return res.item


@router.post(
    "/community/join/",
    responses={
        200: {"model": Community, "description": "OK"},
        401: {"description": "User not active"},
    },
    tags=["Community"],
    summary="Join to community",
    response_model_by_alias=True,
)
async def community_join_by_code(
    code_data: CommunityJoinByCode = Body(None, description=""),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> CommunityRole:
    """Join to community by code"""
    uc = CommunityJoinByCodeUsecase(uow=uow)
    res = await uc(user=current_user, code=code_data.code)
    return res.item


@router.delete(
    "/communities/{community_id}/roles/{user_id}",
    responses={
        200: {"model": Community, "description": "OK"},
        401: {"description": "User not active"},
    },
    tags=["Community"],
    summary="Leave community",
    response_model_by_alias=True,
)
async def community_leave(
    community_id: int = Path(description="community id"),
    user_id: int = Path(description="user id"),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> bool:
    if current_user.id != user_id:
        raise HTTPException(status_code=404)
    uc = CommunityLeaveUsecase(uow=uow)
    res = await uc(user=current_user, community_id=community_id)
    return res.item


@router.patch(
    "/communities/{community_id}/roles/{user_id}",
    responses={
        200: {"model": CommunityRole, "description": "OK"},
        401: {"description": "User not active"},
    },
    tags=["Community"],
    summary="Update community role for specific user",
    response_model_by_alias=True,
)
async def community_role_update(
    community_id: int = Path(description="community id"),
    user_id: int = Path(description="user id"),
    community_role_data: CommunityRoleUpdate = Body(None, description=""),
    current_user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> CommunityRole:
    uc = CommunityChangeUserRoleUsecase(uow=uow)
    res = await uc(
        user=current_user,
        community_id=community_id,
        user_id=user_id,
        update_obj=UserCommunityUpdateDTO(**community_role_data.dict()),
    )
    return res.item
