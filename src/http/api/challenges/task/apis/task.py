from fastapi import APIRouter, Depends, Path, Query

from src.core.dto.mock import MockObj
from src.core.interfaces.repository.challenges.task import TaskFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_get import TaskGetUseCase
from src.core.usecases.challenges.task.task_list import TaskListUseCase
from src.http.api.challenges.task.schemas.task import Task, TaskFilterObject
from src.http.api.depends import get_uow, get_user

router = APIRouter(tags=["Task"])


@router.get(
    "/task/{id}",
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
    "/task",
    responses={
        200: {"model": list[Task], "description": "OK"},
        422: {"description": "User not active"},
    },
    summary="Task list",
    response_model_by_alias=True,
)
async def task_list(
    user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
    filter_obj: TaskFilterObject = Query(default=None, description="Filter object"),
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
