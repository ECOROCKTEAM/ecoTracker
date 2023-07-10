from typing import Annotated

from fastapi import APIRouter, Depends, Path

from src.core.dto.mock import MockObj
from src.core.interfaces.repository.challenges.task import (
    TaskUserFilter,
    TaskUserPlanFilter,
)
from src.core.usecases.challenges.task.task_user_add import UserTaskAddUseCase
from src.core.usecases.challenges.task.task_user_complete import UserTaskCompleteUseCase
from src.core.usecases.challenges.task.task_user_get import UserTaskGetUseCase
from src.core.usecases.challenges.task.task_user_list import UserTaskListUseCase
from src.core.usecases.challenges.task.task_user_plan_list import (
    UserTaskPlanListUseCase,
)
from src.core.usecases.challenges.task.task_user_reject import UserTaskRejectUseCase
from src.http.api.challenges.task.schemas.task import (
    TaskUserEntity,
    TaskUserFilterQueryParams,
    TaskUserPlanEntity,
    TaskUserPlanFilterQueryParams,
)
from src.http.api.deps import get_uow, get_user

router = APIRouter(tags=["Task User"])


@router.get(
    "/tasks/users",
    responses={
        200: {"model": list[TaskUserEntity], "description": "OK"},
        401: {"description": "User not active"},
    },
    summary="List user tasks",
    response_model_by_alias=True,
)
async def task_user_list(
    filter_obj: Annotated[TaskUserFilterQueryParams, Depends()],
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> list[TaskUserEntity]:
    """Get list of user tasks"""
    uc = UserTaskListUseCase(uow=uow)
    result = await uc(
        user=user, order_obj=MockObj(), pagination_obj=MockObj(), filter_obj=TaskUserFilter(**filter_obj.__dict__)
    )
    return result.items


@router.get(
    "/tasks/{id}/users",
    responses={
        200: {"model": TaskUserEntity, "description": "OK"},
        401: {"description": "User not active"},
    },
    summary="Get user task",
    response_model_by_alias=True,
)
async def task_user_get(
    id: int = Path(description="task identify"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> TaskUserEntity:
    """Get user task"""
    uc = UserTaskGetUseCase(uow=uow)
    result = await uc(user=user, obj_id=id)
    return result.item


@router.get(
    "/tasks/users/plans",
    responses={
        200: {"model": list[TaskUserPlanEntity], "description": "OK"},
        401: {"description": "User not active"},
    },
    summary="Your GET endpoint",
    response_model_by_alias=True,
)
async def task_user_plan_list(
    filter_obj: Annotated[TaskUserPlanFilterQueryParams, Depends()],
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> list[TaskUserPlanEntity]:
    """Get User Task Plan list"""
    uc = UserTaskPlanListUseCase(uow=uow)
    result = await uc(
        user=user, filter_obj=TaskUserPlanFilter(**filter_obj.__dict__), order_obj=MockObj(), pagination_obj=MockObj()
    )
    return result.items


@router.post(
    "/tasks/users/{id}",
    responses={
        200: {"description": "OK"},
    },
    summary="Add task to user list",
    response_model_by_alias=True,
)
async def task_user_add(
    id: int = Path(description="task identify"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> TaskUserEntity:
    """Add task to user list"""
    uc = UserTaskAddUseCase(uow=uow)
    result = await uc(user=user, task_id=id)
    return result.item


@router.patch(
    "/tasks/users/complete/{obj_id}",
    responses={
        200: {"model": TaskUserEntity, "description": "OK"},
        401: {"description": "User not active"},
    },
    summary="Complete user task",
    response_model_by_alias=True,
)
async def task_user_complete(
    obj_id: int = Path(description="task identify"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> TaskUserEntity:
    """Complete user task"""
    uc = UserTaskCompleteUseCase(uow=uow)
    result = await uc(user=user, obj_id=obj_id)
    return result.item


@router.patch(
    "/tasks/users/reject/{obj_id}",
    responses={
        200: {"model": TaskUserEntity, "description": "OK"},
        401: {"description": "User not active"},
    },
    summary="Reject User Task",
    response_model_by_alias=True,
)
async def task_user_reject(
    obj_id: int = Path(description="task identify"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> TaskUserEntity:
    """Reject User Task"""
    uc = UserTaskRejectUseCase(uow=uow)
    result = await uc(user=user, obj_id=obj_id)
    return result.item
