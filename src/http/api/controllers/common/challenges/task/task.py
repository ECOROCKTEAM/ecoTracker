from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_get import TaskGetUsecase
from src.core.usecases.challenges.task.task_list import TaskListUsecase
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.challenges.task.task import (
    TaskFilterSchema,
    TaskListSchema,
    TaskSchema,
)
from src.http.api.schemas.utils import IterableSchema, SortSchema

router = APIRouter()


@router.get("/list")
async def task_list(
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
    fltr: TaskFilterSchema = Depends(),
    sorting: SortSchema = Depends(),
    iterable: IterableSchema = Depends(),
) -> TaskListSchema:
    filter_obj = fltr.to_obj()
    sorting_obj = sorting.to_obj()
    iterable_obj = iterable.to_obj()

    uc = TaskListUsecase(uow=uow)
    res = await uc(user=user, filter_obj=filter_obj, sorting_obj=sorting_obj, iterable_obj=iterable_obj)
    return TaskListSchema.from_obj(task_list=res.items, limit=res.limit, offset=res.offset, total=res.total)


@router.get("/{id}")
async def task_get(
    id: int, uow: Annotated[IUnitOfWork, Depends(get_uow_stub)], user: Annotated[User, Depends(get_user_stub)]
) -> TaskSchema:
    uc = TaskGetUsecase(uow=uow)
    result = await uc(user=user, id=id)
    return TaskSchema.from_obj(task=result.item)
