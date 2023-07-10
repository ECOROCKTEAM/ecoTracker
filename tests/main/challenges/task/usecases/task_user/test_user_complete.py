import pytest

from src.core.entity.score import ScoreUser
from src.core.entity.task import Task, TaskUser
from src.core.entity.user import User
from src.core.exception.base import EntityNotChange
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_user_complete import UserTaskCompleteUsecase
from tests.fixtures.challenges.task.usecase.task import mock_task_get_default
from tests.fixtures.challenges.task.usecase.user_task import (
    mock_user_task_add,
    mock_user_task_get_default,
    mock_user_task_get_finish,
    mock_user_task_update,
)
from tests.fixtures.score.usecase.user_score import mock_user_score_add
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/challenges/task/usecases/task_user/test_user_complete.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_task_get_default: Task,
    mock_user_task_get_default: TaskUser,
    mock_user_task_add: TaskUser,
    mock_user_task_update: Task,
    mock_user_score_add: ScoreUser,
):
    uc = UserTaskCompleteUsecase(uow=uow)
    res = await uc(user=fxe_user_default, id=1)
    task = res.item
    assert isinstance(task, TaskUser)
    assert task.id == mock_user_task_add.id


# pytest tests/main/challenges/task/usecases/task_user/test_user_complete.py::test_not_active -v -s
@pytest.mark.asyncio
async def test_not_active(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_task_get_default: Task,
    mock_user_task_get_finish: TaskUser,
):
    uc = UserTaskCompleteUsecase(uow=uow)
    with pytest.raises(EntityNotChange):
        await uc(user=fxe_user_default, id=1)
