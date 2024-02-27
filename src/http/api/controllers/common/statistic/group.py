from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.statistic.group_mission_counter import (
    GroupMissionCounterStatisticUsecase,
)
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.statistic.common import OccupancyStatisticFilterSchema
from src.http.api.schemas.statistic.group import GroupMissionCounterSchema

router = APIRouter()


@router.get("/{group_id}/mission/counter")
async def group_mission_counter(
    group_id: int,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
    fltr: OccupancyStatisticFilterSchema = Depends(),
) -> GroupMissionCounterSchema:
    """"""
    filter_obj = fltr.to_obj()

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    result = await uc(user=user, group_id=group_id, filter_obj=filter_obj)
    return GroupMissionCounterSchema.from_obj(group_mission_counter=result.item)
