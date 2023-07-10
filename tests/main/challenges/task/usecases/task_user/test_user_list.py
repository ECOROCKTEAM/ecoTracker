import pytest

from src.core.dto.mock import MockObj
from src.core.entity.task import TaskUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.challenges.task import TaskUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_user_list import UserTaskListUsecase
from tests.fixtures.challenges.task.usecase.user_task import mock_user_task_check_filter
from tests.fixtures.const import DEFAULT_TEST_USECASE_TASK_ID
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/challenges/task/usecases/task_user/test_user_list.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_user_task_check_filter: list[TaskUser],
):
    uc = UserTaskListUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        filter_obj=TaskUserFilter(task_id=1, task_active=True, status=OccupancyStatusEnum.ACTIVE),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    tasks = res.item
    assert isinstance(tasks, list)
    assert len(tasks) == 1
    task = tasks[0]
    assert isinstance(task, TaskUser)
    assert task.id == DEFAULT_TEST_USECASE_TASK_ID
