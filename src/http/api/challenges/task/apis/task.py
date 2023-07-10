from typing import Annotated

from fastapi import APIRouter, Depends, Path

from src.core.dto.mock import MockObj
from src.core.interfaces.repository.challenges.task import (
    TaskFilter,
    TaskFilterQueryParams,
)
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_get import TaskGetUseCase
from src.core.usecases.challenges.task.task_list import TaskListUseCase
from src.http.api.challenges.task.schemas.task import Task
from src.http.api.deps import get_uow, get_user

router = APIRouter(tags=["Task"])


@router.get(
    "/tasks/{id}",
    responses={
        200: {"model": Task, "description": "OK"},
        422: {"description": "User not active"},
    },
    summary="Get task",
    response_model_by_alias=True,
)
async def task_get(
    id: int = Path(description="task identify"),
    user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> Task:
    """Get task by ID"""
    uc = TaskGetUseCase(uow=uow)
    result = await uc(user=user, task_id=id)
    return result.item


@router.get(
    "/tasks",
    responses={
        200: {"model": list[Task], "description": "OK"},
        422: {"description": "User not active"},
    },
    summary="Task list",
    response_model_by_alias=True,
)
async def task_list(
    filter_obj: Annotated[TaskFilterQueryParams, Depends()],
    user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> list[Task]:
    """Get task list"""
    uc = TaskListUseCase(uow=uow)
    result = await uc(
        user=user,
        sorting_obj=MockObj(),
        paggination_obj=MockObj(),
        filter_obj=TaskFilter(**filter_obj.__dict__),
    )
    return result.items
