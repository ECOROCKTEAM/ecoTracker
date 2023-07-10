from typing import Annotated

from fastapi import APIRouter, Depends, Path

from src.core.dto.mock import MockObj
from src.core.interfaces.repository.challenges.mission import MissionFilter
from src.core.usecases.challenges.mission.mission_get import MissionGetUsecase
from src.core.usecases.challenges.mission.mission_list import MissionListUsecase
from src.http.api.challenges.mission.schemas.mission import (
    MissionEntity,
    MissionFilterQueryParams,
)
from src.http.api.deps import get_uow, get_user

router = APIRouter(tags=["Mission"])


@router.get(
    "/missions/{mission_id}",
    responses={
        200: {"model": MissionEntity, "description": "OK"},
        403: {"description": "User is not premium"},
        404: {"description": "Mission not active"},
    },
    summary="Get mission",
    response_model_by_alias=True,
)
async def mission_get(
    mission_id: int = Path(description="mission identify"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> MissionEntity:
    """Get mission by id"""
    uc = MissionGetUsecase(uow=uow)
    result = await uc(user=user, id=mission_id)
    return result.item


@router.get(
    "/missions",
    responses={
        200: {"model": list[MissionEntity], "description": "OK"},
        403: {"description": "User is not premium"},
    },
    summary="Mission list",
    response_model_by_alias=True,
)
async def mission_list(
    obj: Annotated[MissionFilterQueryParams, Depends()],
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> list[MissionEntity]:
    """Get mission list with filter, pagination, order objects"""
    uc = MissionListUsecase(uow=uow)
    result = await uc(
        user=user, filter_obj=MissionFilter(**obj.__dict__), order_obj=MockObj(), pagination_obj=MockObj()
    )
    return result.item
