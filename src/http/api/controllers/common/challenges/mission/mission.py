from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_get import MissionGetUsecase
from src.core.usecases.challenges.mission.mission_list import MissionListUsecase
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.challenges.mission.mission import (
    MissionFilterSchema,
    MissionListSchema,
    MissionSchema,
    MissionSortingSchema,
)
from src.http.api.schemas.utils import IterableSchema

router = APIRouter()


@router.get("/list")
async def mission_list(
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
    flrt: MissionFilterSchema = Depends(),
    sorting: MissionSortingSchema = Depends(),
    iterable: IterableSchema = Depends(),
) -> MissionListSchema:
    filter_obj = flrt.to_obj()
    sorting_obj = sorting.to_obj()
    iterable_obj = iterable.to_obj()

    uc = MissionListUsecase(uow=uow)
    res = await uc(user=user, filter_obj=filter_obj, sorting_obj=sorting_obj, iterable_obj=iterable_obj)
    return MissionListSchema.from_obj(mission_list=res.items, offset=res.offset, total=res.total, limit=res.limit)


@router.get("/{id}")
async def mission_get(
    id: int,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
) -> MissionSchema:
    uc = MissionGetUsecase(uow=uow)
    res = await uc(user=user, id=id)
    return MissionSchema.from_obj(item=res.item)
