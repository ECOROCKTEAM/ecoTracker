import pytest

from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.exception.base import EntityNotFound
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_user_get import UserTaskGetUsecase
from tests.fixtures.challenges.task.usecase.user_task import mock_user_task_get_default
from tests.fixtures.const import DEFAULT_TEST_USECASE_TASK_ID
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/challenges/task/usecases/task_user/test_user_get.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_user_task_get_default: TaskUser,
):
    uc = UserTaskGetUsecase(uow=uow)
    res = await uc(user=fxe_user_default, id=1)
    task = res.item
    assert isinstance(task, TaskUser)
    assert task.id == DEFAULT_TEST_USECASE_TASK_ID


# pytest tests/challenges/task/usecases/task_user/test_user_get.py::test_not_found -v -s
@pytest.mark.asyncio
async def test_not_found(
    uow: IUnitOfWork,
    fxe_user_default: User,
    # mock_user_task_get_default: TaskUser,
):
    uc = UserTaskGetUsecase(uow=uow)
    with pytest.raises(EntityNotFound):
        await uc(user=fxe_user_default, id=-1)
