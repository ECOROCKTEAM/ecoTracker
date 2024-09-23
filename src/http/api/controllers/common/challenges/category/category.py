from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.occupancy.occupancy_list import CategoryListUsecase
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.challenges.category.category import (
    OccupancyFilterSchema,
    OccupancyListSchema,
)

router = APIRouter()


@router.get("/list")
async def occupancy_list(
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    fltr: OccupancyFilterSchema = Depends(),
) -> OccupancyListSchema:
    fltr_obj = fltr.to_obj()

    uc = CategoryListUsecase(uow=uow)
    res = await uc(user=user, fltr=fltr_obj)
    return OccupancyListSchema.from_obj(occupancy_list=res.item)
