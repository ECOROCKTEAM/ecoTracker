from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_user_add import UserTaskAddUsecase
from src.core.usecases.challenges.task.task_user_complete import UserTaskCompleteUsecase
from src.core.usecases.challenges.task.task_user_get import UserTaskGetUsecase
from src.core.usecases.challenges.task.task_user_list import UserTaskListUsecase
from src.core.usecases.challenges.task.task_user_reject import UserTaskRejectUsecase
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.challenges.task.task_user import (
    SortUserTaskSchema,
    TaskUserFilterSchema,
    TaskUserListSchema,
    TaskUserSchema,
)
from src.http.api.schemas.utils import IterableSchema

router = APIRouter()


@router.get("/list")
async def task_user_list(
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    fltr: TaskUserFilterSchema = Depends(),
    sorting: SortUserTaskSchema = Depends(),
    iterable: IterableSchema = Depends(),
) -> TaskUserListSchema:
    filter_obj = fltr.to_obj()
    sorting_obj = sorting.to_obj()
    iterable_obj = iterable.to_obj()

    uc = UserTaskListUsecase(uow=uow)
    res = await uc(user=user, filter_obj=filter_obj, sorting_obj=sorting_obj, iterable_obj=iterable_obj)
    return TaskUserListSchema.from_obj(task_user_list=res.items, limit=res.limit, offset=res.offset, total=res.total)


@router.get("/{task_user_id}")
async def task_user_get(
    task_user_id: int,
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
) -> TaskUserSchema:
    uc = UserTaskGetUsecase(uow=uow)
    res = await uc(user=user, id=task_user_id)
    return TaskUserSchema.from_obj(task_user=res.item)


@router.post("/")
async def task_user_add(
    task_id: int, user: Annotated[User, Depends(get_user_stub)], uow: Annotated[IUnitOfWork, Depends(get_uow_stub)]
) -> TaskUserSchema:
    uc = UserTaskAddUsecase(uow=uow)
    res = await uc(user=user, task_id=task_id)
    return TaskUserSchema.from_obj(task_user=res.item)


@router.patch("/complete/{task_user_id}")
async def task_user_complete(
    task_user_id: int, user: Annotated[User, Depends(get_user_stub)], uow: Annotated[IUnitOfWork, Depends(get_uow_stub)]
) -> TaskUserSchema:
    uc = UserTaskCompleteUsecase(uow=uow)
    res = await uc(user=user, id=task_user_id)
    return TaskUserSchema.from_obj(task_user=res.item)


@router.patch("/reject/{task_user_id}")
async def task_user_reject(
    task_user_id: int, user: Annotated[User, Depends(get_user_stub)], uow: Annotated[IUnitOfWork, Depends(get_uow_stub)]
) -> TaskUserSchema:
    uc = UserTaskRejectUsecase(uow=uow)
    res = await uc(user=user, id=task_user_id)
    return TaskUserSchema.from_obj(task_user=res.item)
