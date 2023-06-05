from fastapi import APIRouter, Depends, Path

from endpoints.dep import get_uow, get_user
from endpoints.schemas import OccupancyCategorySchema

router = APIRouter(tags=["Occupancy"])


@router.get(
    "/occupancy/get/{id}",
    responses={
        200: {"model": OccupancyCategorySchema, "description": "OK"},
        403: {"description": "User is not active"},
    },
    summary="Get occupancy category",
    response_model_by_alias=True,
)
async def get_occupancy_get_id(
    id: int = Path(None, description="occupancy id"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> OccupancyCategorySchema:
    """Get occupancy"""


@router.get(
    "/occupancy/list",
    responses={
        200: {"model": list[OccupancyCategorySchema], "description": "OK"},
        403: {"description": "User is not active"},
    },
    summary="List occupancy category",
    response_model_by_alias=True,
)
async def get_occupancy_list() -> list[OccupancyCategorySchema]:
    """Get list occupancy category"""
