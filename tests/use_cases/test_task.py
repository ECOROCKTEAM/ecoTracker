from dataclasses import asdict
from datetime import datetime, timedelta

import pytest

from src.core.dto.challenges.task import TaskUserUpdateDTO
from src.core.dto.mock import MockObj
from src.core.entity.task import Task
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum
from src.core.interfaces.repository.challenges.task import (
    TaskFilter,
    TaskUserFilter,
    TaskUserPlanFilter,
)
from src.core.usecases.challenges.task import (
    task_get,
    task_list,
    task_user_add,
    task_user_complete,
    task_user_delete,
    task_user_get,
    task_user_list,
    task_user_plan_list,
    task_user_update,
)
from src.data.unit_of_work import SqlAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_list(pool, test_task_model_list, test_user: User):
    lang = LanguageEnum.RU
    test_user.language = lang
    test_task_ids = [m.id for m in test_task_model_list]
    uow = SqlAlchemyUnitOfWork(pool)
    uc = task_list.TaskListUseCase(uow=uow)
    result = await uc(user=test_user, sorting_obj=MockObj(), paggination_obj=MockObj(), filter_obj=TaskFilter())
    assert isinstance(result.items, list)
    for task in result.items:
        assert task.id in test_task_ids
        assert task.language == lang


@pytest.mark.asyncio
async def test_get(pool, test_task: Task, test_user: User):
    test_user.language = test_task.language
    uow = SqlAlchemyUnitOfWork(pool)
    uc = task_get.TaskGetUseCase(uow=uow)
    result = await uc(user=test_user, task_id=test_task.id)
    task = result.item
    assert test_task.id == task.id
    assert test_task.score == task.score
    assert test_task.name == task.name
    assert test_task.description == task.description
    assert test_task.language == task.language


@pytest.mark.asyncio
async def test_user_task_get(pool, test_user: User, test_task: Task, test_user_task):
    test_user.language = test_task.language
    uow = SqlAlchemyUnitOfWork(pool)
    uc = task_user_get.UserTaskGetUseCase(uow=uow)
    result = await uc(user=test_user, task_id=test_task.id)
    user_task = result.item
    assert test_user.id == user_task.user_id
    assert test_task.id == user_task.task_id


@pytest.mark.asyncio
async def test_user_task_lst(pool, test_user: User):
    test_user.language = LanguageEnum.EN
    uow = SqlAlchemyUnitOfWork(pool)
    uc = task_user_list.UserTaskListUseCase(uow=uow)
    result = await uc(user=test_user, filter_obj=TaskUserFilter(), order_obj=MockObj(), pagination_obj=MockObj())
    user_task_list = result.items
    for obj in user_task_list:
        assert obj.user_id == test_user.id


# @pytest.mark.asyncio
# async def test_user_task_update(pool, test_user: User, test_task: Task):
#     test_user.language = test_task.language
#     t = datetime.now() - timedelta(hours=1)
#     update_obj = TaskUserUpdateDTO(date_close=t, status=OccupancyStatusEnum.OVERDUE)
#     uow = SqlAlchemyUnitOfWork(pool)
#     uc = task_user_update.UserTaskUpdateUseCase(uow=uow)
#     result = await uc(user=test_user, task_id=test_task.id, obj=update_obj)
#     upd_obj = result.item
#     assert upd_obj.task_id == test_task.id
#     assert upd_obj.user_id == test_user.id
#     assert upd_obj.status == update_obj.status
#     # assert upd_obj.date_close == update_obj.date_close
#     # time\time+00:00 - Спросить


@pytest.mark.asyncio
async def test_plan_list(pool, test_user: User, test_task: Task):
    test_user.language = test_task.language
    uow = SqlAlchemyUnitOfWork(pool)
    uc = task_user_plan_list.UserTaskPlanListUseCase(uow=uow)
    result = await uc(
        user=test_user,
        filter_obj=TaskUserPlanFilter(),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    plan_list = result.items
    for obj in plan_list:
        assert test_user.id == obj.user_id
        assert test_task.id == obj.task_id


@pytest.mark.asyncio
async def test_user_task_add(pool, test_task2: Task, test_user: User, test_user_task2):
    test_user.language = test_task2.language
    uow = SqlAlchemyUnitOfWork(pool)
    uc = task_user_add.UserTaskAddUseCase(uow=uow)
    result = await uc(user=test_user, task_id=test_task2.id)
    user_task = result.item
    assert user_task.user_id == test_user.id
    assert user_task.task_id == test_task2.id


# @pytest.mark.asyncio
# async def test_task_complete(pool, test_user_task, test_user, test_task):
#     test_user.language = test_task.language
#     uow = SqlAlchemyUnitOfWork(pool)
#     uc = task_user_complete.UserTaskCompleteUseCase(uow=uow)
#     result = await uc(user=test_user, task_id=test_task.id)
#     user_task = result.item
#     assert user_task.user_id == test_user.id
#     assert user_task.task_id == test_task.id
#     assert user_task.status == OccupancyStatusEnum.FINISH
#     # assert user_task.date_close == test_user_task.date_close Как правильно даты проверить?
#     # assert user_task.date_start == test_user_task.date_start


# @pytest.mark.asyncio
# async def test_task_delete(pool, test_user_task, test_user, test_task):
#     print(test_user_task)
#     test_user.language = test_task.language
#     uow = SqlAlchemyUnitOfWork(pool)
#     uc = task_user_delete.UserTaskDeleteUseCase(uow=uow)
#     result = await uc(user=test_user, task_id=test_task.id)
#     user_task = result.item
#     assert user_task.user_id == test_user.id
#     assert user_task.task_id == test_task.id
#     assert isinstance(user_task.date_close, datetime)
