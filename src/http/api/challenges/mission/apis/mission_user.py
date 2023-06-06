from fastapi import APIRouter, Body, Depends, Path, Query

from src.core.dto.challenges.mission import MissionUserCreateDTO, MissionUserUpdateDTO
from src.core.dto.mock import MockObj
from src.core.interfaces.repository.challenges.mission import MissionUserFilter
from src.core.usecases.challenges.mission.mission_user_create import (
    MissionUserCreateUsecase,
)
from src.core.usecases.challenges.mission.mission_user_get import MissionUserGetUsecase
from src.core.usecases.challenges.mission.mission_user_list import (
    MissionUserListUsecase,
)
from src.core.usecases.challenges.mission.mission_user_update import (
    MissionUserUpdateUsecase,
)
from src.http.api.challenges.mission.schemas.mission_user import (
    MissionUserCreateObject,
    MissionUserEntity,
    MissionUserFilterObject,
    MissionUserUpdateObject,
)
from src.http.api.depends import get_uow, get_user

router = APIRouter(tags=["Mission User"])


@router.get(
    "/mission/user/{id}",
    responses={
        200: {"model": MissionUserEntity, "description": "OK"},
        403: {"description": "User is not premium"},
    },
    summary="Get user mission",
    response_model_by_alias=True,
)
async def get(
    id: int = Path(description="object id"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> MissionUserEntity:
    """Get user mission"""
    uc = MissionUserGetUsecase(uow=uow)
    result = await uc(user=user, id=id)
    return result.item


@router.get(
    "/mission/user",
    responses={
        200: {"model": list[MissionUserEntity], "description": "OK"},
        403: {"description": "User is not premium"},
    },
    tags=["Mission User"],
    summary="User mission list",
    response_model_by_alias=True,
)
async def lst(
    obj: MissionUserFilterObject = Query(None, description=""),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> list[MissionUserEntity]:
    """Get user mission list"""
    uc = MissionUserListUsecase(uow=uow)
    result = await uc(
        user=user, filter_obj=MissionUserFilter(**obj.dict()), order_obj=MockObj(), pagination_obj=MockObj()
    )
    return result.item


@router.patch(
    "/mission/user/{id}",
    responses={
        200: {"model": MissionUserEntity, "description": "OK"},
        403: {"description": "User is not premium"},
        404: {"description": "Mission status is not Active"},
    },
    tags=["Mission User"],
    summary="Update user mission",
    response_model_by_alias=True,
)
async def patch(
    id: int = Path(description="updating object id"),
    obj: MissionUserUpdateObject = Body(None, description="Updating object"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> MissionUserEntity:
    """Updating user mission object"""
    uc = MissionUserUpdateUsecase(uow=uow)
    result = await uc(user=user, id=id, update_obj=MissionUserUpdateDTO(**obj.dict()))
    return result.item


@router.post(
    "/mission/user",
    responses={
        200: {"model": MissionUserEntity, "description": "OK"},
        403: {"description": "User is not premium"},
        404: {"description": "Mission is not active"},
    },
    tags=["Mission User"],
    summary="Create user mission",
    response_model_by_alias=True,
)
async def create(
    obj: MissionUserCreateObject = Body(None, description="Creating obj"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> MissionUserEntity:
    """Create user mission object"""
    uc = MissionUserCreateUsecase(uow=uow)
    result = await uc(user=user, create_obj=MissionUserCreateDTO(**obj.dict()))
    return result.item
