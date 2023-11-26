from fastapi import APIRouter  # , Depends, Path

# from src.core.usecases.challenges.occupancy.occupancy_get import (
#     OccupancyCategoryGetUsecase,
# )
# from src.core.usecases.challenges.occupancy.occupancy_list import (
#     OccupancyCategoryListUsecase,
# )

# # from src.http.api.dep import get_uow, get_user
# from src.http.api.occupancy.schemas.schemas import OccupancyCategorySchema

router = APIRouter(tags=["Occupancy"])


# @router.get(
#     "/occupancies/{id}",
#     responses={
#         200: {"model": OccupancyCategorySchema, "description": "OK"},
#         403: {"description": "User is not active"},
#     },
#     summary="Get occupancy category",
#     response_model_by_alias=True,
# )
# async def occupancy_get(
#     id: int = Path(description="occupancy id"),
#     user=Depends(get_user),
#     uow=Depends(get_uow),
# ) -> OccupancyCategorySchema:
#     """Get occupancy"""
#     uc = OccupancyCategoryGetUsecase(uow=uow)
#     result = await uc(user=user, id=id)
#     return result.item


# @router.get(
#     "/occupancies",
#     responses={
#         200: {"model": list[OccupancyCategorySchema], "description": "OK"},
#         403: {"description": "User is not active"},
#     },
#     summary="List occupancy category",
#     response_model_by_alias=True,
# )
# async def occupancy_list(
#     user=Depends(get_user),
#     uow=Depends(get_uow),
# ) -> list[OccupancyCategorySchema]:
#     """Get list occupancy category"""
#     uc = OccupancyCategoryListUsecase(uow=uow)
#     result = await uc(user=user)
#     return result.items
