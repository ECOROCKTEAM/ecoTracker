from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.statistic.user_mission_counter import (
    UserMissionCounterStatisticUsecase,
)
from src.core.usecases.statistic.user_task_counter import (
    UserTaskCounterStatisticUsecase,
)
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.statistic.common import OccupancyStatisticFilterSchema
from src.http.api.schemas.statistic.user import (
    UserMissionCounterSchema,
    UserTaskCounterSchema,
)

router = APIRouter()


@router.get("/task/counter")
async def user_task_counter(
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    fltr: OccupancyStatisticFilterSchema = Depends(),
) -> UserTaskCounterSchema:
    filter_obj = fltr.to_obj()

    uc = UserTaskCounterStatisticUsecase(uow=uow)
    result = await uc(user=user, filter_obj=filter_obj)
    return UserTaskCounterSchema.from_obj(user_tasks_counter=result.item)


@router.get("/mission/counter")
async def user_mission_counter(
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    fltr: OccupancyStatisticFilterSchema = Depends(),
) -> UserMissionCounterSchema:
    filter_obj = fltr.to_obj()

    uc = UserMissionCounterStatisticUsecase(uow=uow)
    result = await uc(user=user, filter_obj=filter_obj)
    return UserMissionCounterSchema.from_obj(user_mission_counter=result.item)
