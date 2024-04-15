from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
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
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.challenges.mission.mission_group import (
    MissionGroupCreateSchema,
    MissionGroupFilterSchema,
    MissionGroupListSchema,
    MissionGroupSchema,
    MissionGroupSortingSchema,
    MissionGroupUpdateSchema,
)
from src.http.api.schemas.utils import IterableSchema

router = APIRouter()


@router.get("/group/mission/list")
async def mission_group_list(
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
    fltr: MissionGroupFilterSchema = Depends(),
    sorting: MissionGroupSortingSchema = Depends(),
    iterable: IterableSchema = Depends(),
) -> MissionGroupListSchema:
    filter_obj = fltr.to_obj()
    sorting_obj = sorting.to_obj()
    iterable_obj = iterable.to_obj()

    uc = MissionGroupListUsecase(uow=uow)
    res = await uc(user=user, filter_obj=filter_obj, sorting_obj=sorting_obj, iterable_obj=iterable_obj)
    return MissionGroupListSchema.from_obj(
        mission_group_list=res.items, limit=res.limit, offset=res.offset, total=res.total
    )


@router.get("/group/{group_id}/mission/{mission_id}")
async def mission_group_get(
    mission_id: int,
    group_id: int,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
) -> MissionGroupSchema:
    uc = MissionGroupGetUsecase(uow=uow)
    res = await uc(user=user, id=mission_id, group_id=group_id)
    return MissionGroupSchema.from_obj(mission_group=res.item)


@router.post("/group/mission")
async def mission_group_create(
    group_id: int,
    in_obj: MissionGroupCreateSchema,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
) -> MissionGroupSchema:
    obj = in_obj.to_obj()
    uc = MissionGroupCreateUsecase(uow=uow)
    res = await uc(user=user, group_id=group_id, create_obj=obj)
    return MissionGroupSchema.from_obj(mission_group=res.item)


@router.patch("/group/mission")
async def mission_group_update(
    mission_id: int,
    group_id: int,
    in_obj: MissionGroupUpdateSchema,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
) -> MissionGroupSchema:
    obj = in_obj.to_obj()
    uc = MissionGroupUpdateUsecase(uow=uow)
    res = await uc(user=user, id=mission_id, group_id=group_id, update_obj=obj)
    return MissionGroupSchema.from_obj(mission_group=res.item)
