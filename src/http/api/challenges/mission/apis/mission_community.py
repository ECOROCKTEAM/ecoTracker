from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query

from src.core.dto.challenges.mission import (
    MissionCommunityCreateDTO,
    MissionCommunityUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.interfaces.repository.challenges.mission import MissionCommunityFilter
from src.core.usecases.challenges.mission.mission_community_create import (
    MissionCommunityCreateUsecase,
)
from src.core.usecases.challenges.mission.mission_community_get import (
    MissionCommunityGetUsecase,
)
from src.core.usecases.challenges.mission.mission_community_list import (
    MissionCommunityListUsecase,
)
from src.core.usecases.challenges.mission.mission_community_update import (
    MissionCommunityUpdateUsecase,
)
from src.http.api.challenges.mission.schemas.mission_community import (
    MissionCommunityCreateObject,
    MissionCommunityEntity,
    MissionCommunityUpdateObject,
    mission_community_filter_query_params,
)
from src.http.api.depends import get_uow, get_user

router = APIRouter(
    tags=["Mission Community"],
)


@router.get(
    "/mission/community",
    responses={
        200: {"model": list[MissionCommunityEntity], "description": "OK"},
        403: {"description": "User is not premium"},
    },
    summary="Mission community list",
    response_model_by_alias=True,
)
async def mission_community_list(
    filter_obj: Annotated[dict, Depends(mission_community_filter_query_params)],
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> list[MissionCommunityEntity]:
    """Mission community list"""
    uc = MissionCommunityListUsecase(uow=uow)
    result = await uc(
        user=user,
        filter_obj=MissionCommunityFilter(**filter_obj),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    return result.item


@router.get(
    "/mission/community/{id}",
    responses={
        200: {"model": MissionCommunityEntity, "description": "OK"},
        403: {"description": "User is not premium"},
    },
    summary="Mission community",
    response_model_by_alias=True,
)
async def mission_community_get(
    id: int = Path(description="object id"),
    community_id: int = Path(description="community id"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> MissionCommunityEntity:
    """Get mission community"""
    uc = MissionCommunityGetUsecase(uow=uow)
    result = await uc(user=user, id=id, community_id=community_id)
    return result.item


@router.patch(
    "/mission/community/{id}",
    responses={
        200: {"model": MissionCommunityEntity, "description": "OK"},
        404: {"description": "Entity not found or not changed"},
    },
    summary="Update mission community",
    response_model_by_alias=True,
)
async def mission_community_update(
    id: int = Path(description="object id"),
    community_id: int = Query(description="community_id"),
    obj: MissionCommunityUpdateObject = Body(default=None, description=""),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> MissionCommunityEntity:
    """Update mission community object"""
    uc = MissionCommunityUpdateUsecase(uow=uow)
    result = await uc(
        user=user,
        id=id,
        community_id=community_id,
        update_obj=MissionCommunityUpdateDTO(**obj.dict()),
    )
    return result.item


@router.post(
    "/mission/community/",
    responses={
        200: {"model": MissionCommunityEntity, "description": "OK"},
        403: {"description": "User is not premium or user has not permission for creating community mission"},
        404: {"description": "Entity not active"},
    },
    summary="Mission Community create",
    response_model_by_alias=True,
)
async def mission_community_create(
    id: int = Query(description="community_id"),
    obj: MissionCommunityCreateObject = Body(default=None, description=""),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> MissionCommunityEntity:
    """Mission Community create"""
    uc = MissionCommunityCreateUsecase(uow=uow)
    result = await uc(user=user, community_id=id, create_obj=MissionCommunityCreateDTO(**obj.dict()))
    return result.item
