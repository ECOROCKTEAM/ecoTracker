import pytest

from src.core.dto.mock import MockObj
from src.core.entity.task import Task
from src.core.entity.user import User
from src.core.interfaces.repository.challenges.task import TaskFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_list import TaskListUsecase
from tests.fixtures.challenges.task.usecase.task import mock_task_lst_check_filter
from tests.fixtures.user.usecase.entity import fxe_user_default


# python -m pytest tests/challenges/task/usecases/task/test_list.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_task_lst_check_filter,
):
    uc = TaskListUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        filter_obj=TaskFilter(active=False),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    # active filter was changed to true
    task_list = res.item
    assert len(task_list) == 0
