from fastapi import APIRouter, Body, Depends, Path, Query

from src.core.dto.challenges.mission import MissionGroupCreateDTO, MissionGroupUpdateDTO
from src.core.dto.mock import MockObj
from src.core.interfaces.repository.challenges.mission import MissionGroupFilter
from src.core.usecases.challenges.mission.mission_group_create import (
    MissionGroupCreateUsecase,
)
from src.core.usecases.challenges.mission.mission_group_get import (
    MissionGroupGetUsecase,
)
from src.core.usecases.challenges.mission.mission_group_list import (
    MissionGroupListUsecase,
)
from src.core.usecases.challenges.mission.mission_group_update import (
    MissionGroupUpdateUsecase,
)
from src.http.api.challenges.mission.schemas.mission_group import (
    MissionGroupCreateObject,
    MissionGroupEntity,
    MissionGroupFilterObject,
    MissionGroupUpdateObject,
)
from src.http.api.depends import get_uow, get_user

router = APIRouter(
    tags=["Mission Group"],
)


@router.get(
    "/mission/groups",
    responses={
        200: {"model": list[MissionGroupEntity], "description": "OK"},
        403: {"description": "User is not premium"},
    },
    summary="Mission group list",
    response_model_by_alias=True,
)
async def mission_group_list(
    filter_obj: MissionGroupFilterObject = Query(default=None, description=""),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> list[MissionGroupEntity]:
    """Mission group list"""
    uc = MissionGroupListUsecase(uow=uow)
    result = await uc(
        user=user,
        filter_obj=MissionGroupFilter(**filter_obj.dict()),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    return result.item


@router.get(
    "/mission/groups/{id}",
    responses={
        200: {"model": MissionGroupEntity, "description": "OK"},
        403: {"description": "User is not premium"},
    },
    summary="Mission group",
    response_model_by_alias=True,
)
async def mission_group_get(
    id: int = Path(description="object id"),
    group_id: int = Path(description="Group id"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> MissionGroupEntity:
    """Get mission group"""
    uc = MissionGroupGetUsecase(uow=uow)
    result = await uc(user=user, id=id, group_id=group_id)
    return result.item


@router.patch(
    "/mission/groups/{id}",
    responses={
        200: {"model": MissionGroupEntity, "description": "OK"},
        404: {"description": "Entity not found or not changed"},
    },
    summary="Update mission group",
    response_model_by_alias=True,
)
async def mission_group_update(
    id: int = Path(description="object id"),
    group_id: int = Query(description="group_id"),
    obj: MissionGroupUpdateObject = Body(default=None, description=""),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> MissionGroupEntity:
    """Update mission group object"""
    uc = MissionGroupUpdateUsecase(uow=uow)
    result = await uc(
        user=user,
        id=id,
        group_id=group_id,
        update_obj=MissionGroupUpdateDTO(**obj.dict()),
    )
    return result.item


@router.post(
    "/mission/groups/",
    responses={
        200: {"model": MissionGroupEntity, "description": "OK"},
        403: {"description": "User is not premium or user has not permission for creating group mission"},
        404: {"description": "Entity not active"},
    },
    summary="Mission group create",
    response_model_by_alias=True,
)
async def mission_group_create(
    id: int = Query(description="group_id"),
    obj: MissionGroupCreateObject = Body(default=None, description=""),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> MissionGroupEntity:
    """Mission Group create"""
    uc = MissionGroupCreateUsecase(uow=uow)
    result = await uc(user=user, group_id=id, create_obj=MissionGroupCreateDTO(**obj.dict()))
    return result.item
