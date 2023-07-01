import pytest

from src.core.entity.task import Task
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_get import TaskGetUsecase
from tests.fixtures.challenges.task.usecase.task import (
    mock_task_get_default,
    mock_task_not_active,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/challenges/task/usecases/task/test_get.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_task_get_default: Task,
):
    uc = TaskGetUsecase(uow=uow)
    res = await uc(user=fxe_user_default, id=1)
    task = res.item
    assert isinstance(task, Task)
    assert mock_task_get_default.id == task.id
    assert mock_task_get_default.active == task.active
    assert mock_task_get_default.score == task.score
    assert mock_task_get_default.description == task.description
    assert mock_task_get_default.category_id == task.category_id
    assert mock_task_get_default.language == task.language


# pytest tests/main/challenges/task/usecases/task/test_get.py::test_not_active -v -s
@pytest.mark.asyncio
async def test_not_active(uow: IUnitOfWork, fxe_user_default: User, mock_task_not_active: Task):
    assert mock_task_not_active.active is False
    uc = TaskGetUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        _ = await uc(user=fxe_user_default, id=1)
