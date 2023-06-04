from fastapi import APIRouter, Body, Depends, Path

from src.core.dto.mock import MockObj
from src.core.http.api.challenges.task.schemas.task import Task, TaskFilterObject
from src.core.http.api.depends import get_uow, get_user
from src.core.interfaces.repository.challenges.task import TaskFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_get import TaskGetUseCase
from src.core.usecases.challenges.task.task_list import TaskListUseCase

router = APIRouter(tags=["Task"])


@router.get(
    "/task/get/{task_id}",
    responses={
        200: {"model": Task, "description": "OK"},
        422: {"description": "User not active"},
    },
    summary="Get task",
    response_model_by_alias=True,
)
async def get(
    task_id: int = Path(default=None, description="task identify"),
    user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> Task:
    """Get task by ID"""
    uc = TaskGetUseCase(uow=uow)
    result = await uc(user=user, task_id=task_id)
    return result.item


@router.get(
    "/task/list",
    responses={
        200: {"model": list[Task], "description": "OK"},
        422: {"description": "User not active"},
    },
    summary="Task list",
    response_model_by_alias=True,
)
async def lst(
    user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
    filter_obj: TaskFilterObject = Body(default=None, description="Filter object"),
) -> list[Task]:
    """Get task list"""
    uc = TaskListUseCase(uow=uow)
    result = await uc(
        user=user,
        sorting_obj=MockObj(),
        paggination_obj=MockObj(),
        filter_obj=TaskFilter(**filter_obj.dict()),
    )
    return result.items
