from fastapi import APIRouter, Body, Depends, Path

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
    TaskUserFilterObject,
    TaskUserPlanEntity,
    TaskUserPlanFilterObject,
)
from src.http.api.depends import get_uow, get_user

router = APIRouter(tags=["Task User"])


@router.get(
    "/task/user/{id}",
    responses={
        200: {"model": TaskUserEntity, "description": "OK"},
        401: {"description": "User not active"},
    },
    summary="Get user task",
    response_model_by_alias=True,
)
async def get(
    id: int = Path(description="task identify"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> TaskUserEntity:
    """Get user task"""
    uc = UserTaskGetUseCase(uow=uow)
    result = await uc(user=user, obj_id=id)
    return result.item


@router.get(
    "/task/user",
    responses={
        200: {"model": list[TaskUserEntity], "description": "OK"},
        401: {"description": "User not active"},
    },
    summary="List user tasks",
    response_model_by_alias=True,
)
async def lst(
    user=Depends(get_user),
    uow=Depends(get_uow),
    filter_obj: TaskUserFilterObject = Body(default=None, description="Filter object"),
) -> list[TaskUserEntity]:
    """Get list of user tasks"""
    uc = UserTaskListUseCase(uow=uow)
    result = await uc(
        user=user, order_obj=MockObj(), pagination_obj=MockObj(), filter_obj=TaskUserFilter(**filter_obj.dict())
    )
    return result.items


@router.get(
    "/task/user/plan",
    responses={
        200: {"model": list[TaskUserPlanEntity], "description": "OK"},
        401: {"description": "User not active"},
    },
    summary="Your GET endpoint",
    response_model_by_alias=True,
)
async def plan_lst(
    user=Depends(get_user),
    uow=Depends(get_uow),
    filter_obj: TaskUserPlanFilterObject = Body(default=None, description="Filter object"),
) -> list[TaskUserPlanEntity]:
    """Get User Task Plan list"""
    uc = UserTaskPlanListUseCase(uow=uow)
    result = await uc(
        user=user, filter_obj=TaskUserPlanFilter(**filter_obj.dict()), order_obj=MockObj(), pagination_obj=MockObj()
    )
    return result.items


@router.post(
    "/task/user/{id}",
    responses={
        200: {"description": "OK"},
    },
    summary="Add task to user list",
    response_model_by_alias=True,
)
async def add(
    id: int = Path(description="task identify"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> TaskUserEntity:
    """Add task to user list"""
    uc = UserTaskAddUseCase(uow=uow)
    result = await uc(user=user, task_id=id)
    return result.item


@router.patch(
    "/task/user/complete/{obj_id}",
    responses={
        200: {"model": TaskUserEntity, "description": "OK"},
        401: {"description": "User not active"},
    },
    summary="Complete user task",
    response_model_by_alias=True,
)
async def complete(
    obj_id: int = Path(description="task identify"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> TaskUserEntity:
    """Complete user task"""
    uc = UserTaskCompleteUseCase(uow=uow)
    result = await uc(user=user, obj_id=obj_id)
    return result.item


@router.patch(
    "/task/user/reject/{obj_id}",
    responses={
        200: {"model": TaskUserEntity, "description": "OK"},
        401: {"description": "User not active"},
    },
    summary="Reject User Task",
    response_model_by_alias=True,
)
async def reject(
    obj_id: int = Path(description="task identify"),
    user=Depends(get_user),
    uow=Depends(get_uow),
) -> TaskUserEntity:
    """Reject User Task"""
    uc = UserTaskRejectUseCase(uow=uow)
    result = await uc(user=user, obj_id=obj_id)
    return result.item
