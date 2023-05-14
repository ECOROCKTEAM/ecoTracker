import pytest
from dataclasses import asdict

from src.core.dto.mock import MockObj
from src.core.entity.task import Task
from src.core.entity.user import User
from src.core.enum.language import LanguageEnum
from src.core.interfaces.repository.challenges.task import TaskFilter
from src.data.unit_of_work import SqlAlchemyUnitOfWork
from src.core.usecases.challenges.task import (
    task_user_add,
    task_list,
    task_get,
)


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
