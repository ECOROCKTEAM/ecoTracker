from fastapi import APIRouter, Depends, Path, Query

from src.core.dto.mock import MockObj
from src.core.interfaces.repository.challenges.mission import MissionFilter
from src.core.usecases.challenges.mission.mission_get import MissionGetUsecase
from src.core.usecases.challenges.mission.mission_list import MissionListUsecase
from src.http.api.challenges.mission.schemas.mission import (
    MissionEntity,
    MissionFilterObject,
)
from src.http.api.depends import get_uow, get_user

router = APIRouter(tags=["Mission"])


@router.get(
    "/mission/{id}",
    responses={
        200: {"model": MissionEntity, "description": "OK"},
        403: {"description": "User is not premium"},
        404: {"description": "Mission not active"},
    },
    summary="Get mission",
    response_model_by_alias=True,
)
async def mission_get(
    id: int = Path(description="mission identify"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> MissionEntity:
    """Get mission by id"""
    uc = MissionGetUsecase(uow=uow)
    result = await uc(user=user, id=id)
    return result.item


@router.get(
    "/mission",
    responses={
        200: {"model": list[MissionEntity], "description": "OK"},
        403: {"description": "User is not premium"},
    },
    summary="Mission list",
    response_model_by_alias=True,
)
async def mission_list(
    user=Depends(get_user),
    uow=Depends(get_uow),
    obj: MissionFilterObject = Query(description="Filter object"),
) -> list[MissionEntity]:
    """Get mission list with filter, pagination, order objects"""
    uc = MissionListUsecase(uow=uow)
    result = await uc(user=user, filter_obj=MissionFilter(**obj.dict()), order_obj=MockObj(), pagination_obj=MockObj())
    return result.item
