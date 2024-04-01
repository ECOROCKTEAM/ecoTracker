from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
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
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.challenges.mission.mission_user import (
    MissionUserCreateSchema,
    MissionUserFilterSchema,
    MissionUserListSchema,
    MissionUserSchema,
    MissionUserSortingSchema,
    MissionUserUpdateSchema,
)
from src.http.api.schemas.utils import IterableSchema

router = APIRouter()


@router.get("/list")
async def mission_user_list(
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
    flrt: MissionUserFilterSchema = Depends(),
    sorting: MissionUserSortingSchema = Depends(),
    iterable: IterableSchema = Depends(),
) -> MissionUserListSchema:
    filter_obj = flrt.to_obj()
    sorting_obj = sorting.to_obj()
    iterable_obj = iterable.to_obj()

    uc = MissionUserListUsecase(uow=uow)
    res = await uc(user=user, filter_obj=filter_obj, sorting_obj=sorting_obj, iterable_obj=iterable_obj)
    return MissionUserListSchema.from_obj(
        mission_user_list=res.items, limit=res.limit, offset=res.offset, total=res.total
    )


@router.get("/{id}")
async def mission_user_get(
    id: int,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
) -> MissionUserSchema:
    uc = MissionUserGetUsecase(uow=uow)
    res = await uc(user=user, id=id)
    return MissionUserSchema.from_obj(mission_user=res.item)


@router.post("/")
async def mission_user_create(
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
    in_obj: MissionUserCreateSchema = Depends(),
) -> MissionUserSchema:
    obj = in_obj.to_obj()
    uc = MissionUserCreateUsecase(uow=uow)
    res = await uc(user=user, create_obj=obj)
    return MissionUserSchema.from_obj(mission_user=res.item)


@router.patch("/{id}")
async def mission_user_update(
    id: int,
    in_obj: MissionUserUpdateSchema,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
) -> MissionUserSchema:
    obj = in_obj.to_obj()
    uc = MissionUserUpdateUsecase(uow=uow)
    res = await uc(user=user, id=id, update_obj=obj)
    return MissionUserSchema.from_obj(mission_user=res.item)
