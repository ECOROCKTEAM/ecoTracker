from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.statistic.user_mission_counter import (
    UserMissionsFinishedCounterUsecase,
)
from src.core.usecases.statistic.user_task_counter import (
    UserTasksFinishedCounterUsecase,
)
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.statistic.common import OccupancyStatisticFilterSchema
from src.http.api.schemas.statistic.user import (
    UserMissionsFinishedSchema,
    UserTasksFinishedSchema,
)

router = APIRouter()


@router.get("/tasks_finished")
async def user_tasks_finished(
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    fltr: OccupancyStatisticFilterSchema = Depends(),
) -> UserTasksFinishedSchema:
    filter_obj = fltr.to_obj()

    uc = UserTasksFinishedCounterUsecase(uow=uow)
    result = await uc(user=user, filter_obj=filter_obj)
    return UserTasksFinishedSchema.from_obj(user_tasks_counter=result.item)


@router.get("/missions_finished")
async def user_mission_finished(
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    fltr: OccupancyStatisticFilterSchema = Depends(),
) -> UserMissionsFinishedSchema:
    """"""
    filter_obj = fltr.to_obj()

    uc = UserMissionsFinishedCounterUsecase(uow=uow)
    result = await uc(user=user, filter_obj=filter_obj)
    return UserMissionsFinishedSchema.from_obj(user_mission_counter=result.item)
