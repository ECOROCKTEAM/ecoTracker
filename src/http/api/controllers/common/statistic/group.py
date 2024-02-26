from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.statistic.group_mission_counter import (
    GroupMissionFinishedCounterUseCase,
)
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.statistic.common import OccupancyStatisticFilterSchema
from src.http.api.schemas.statistic.group import GroupFinishedMissionsSchema

router = APIRouter()


@router.get("/{group_id}/finished_missions")
async def group_finished_missions(
    group_id: int,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
    fltr: OccupancyStatisticFilterSchema = Depends(),
) -> GroupFinishedMissionsSchema:
    """"""
    filter_obj = fltr.to_obj()

    uc = GroupMissionFinishedCounterUseCase(uow=uow)
    result = await uc(user=user, group_id=group_id, filter_obj=filter_obj)
    return GroupFinishedMissionsSchema.from_obj(group_mission_counter=result.item)
