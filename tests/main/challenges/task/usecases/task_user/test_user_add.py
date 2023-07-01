import pytest

from src.core.entity.task import Task, TaskUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityAlreadyUsage, EntityNotActive, MaxAmountError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_user_add import UserTaskAddUsecase
from tests.fixtures.challenges.task.usecase.task import (
    mock_task_get_default,
    mock_task_not_active,
)
from tests.fixtures.challenges.task.usecase.user_task import (
    mock_user_task_add,
    mock_user_task_lst_ret_eq_max_not_premium,
    mock_user_task_lst_ret_eq_max_premium,
    mock_user_task_lst_ret_gt_max_not_premium,
    mock_user_task_lst_ret_gt_max_premium,
    mock_user_task_lst_ret_one,
    mock_user_task_plan_lst_ret_eq_max_not_premium,
    mock_user_task_plan_lst_ret_eq_max_premium,
    mock_user_task_plan_lst_ret_gt_max_not_premium,
    mock_user_task_plan_lst_ret_gt_max_premium,
)
from tests.fixtures.const import DEFAULT_TEST_USECASE_TASK_ID
from tests.fixtures.user.usecase.entity import fxe_user_default, fxe_user_not_premium


# pytest tests/main/challenges/task/usecases/task_user/test_user_add.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_task_get_default: Task,
    mock_user_task_add: TaskUser,
):
    uc = UserTaskAddUsecase(uow=uow)
    res = await uc(user=fxe_user_default, task_id=1)
    task = res.item
    assert isinstance(task, TaskUser)
    assert task.id == mock_user_task_add.id


# pytest tests/main/challenges/task/usecases/task_user/test_user_add.py::test_task_not_active -v -s
@pytest.mark.asyncio
async def test_task_not_active(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_task_not_active: Task,
):
    uc = UserTaskAddUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(user=fxe_user_default, task_id=1)


# pytest tests/main/challenges/task/usecases/task_user/test_user_add.py::test_user_task_already_usage -v -s
@pytest.mark.asyncio
async def test_user_task_already_usage(
    uow: IUnitOfWork, fxe_user_default: User, mock_task_get_default: Task, mock_user_task_lst_ret_one: list[Task]
):
    uc = UserTaskAddUsecase(uow=uow)
    with pytest.raises(EntityAlreadyUsage):
        await uc(user=fxe_user_default, task_id=DEFAULT_TEST_USECASE_TASK_ID)


# pytest tests/main/challenges/task/usecases/task_user/test_user_add.py::test_user_not_premium_max_amount_error -v -s
@pytest.mark.asyncio
async def test_user_not_premium_max_amount_error(
    uow: IUnitOfWork,
    fxe_user_not_premium: User,
    mock_task_get_default: Task,
    mock_user_task_lst_ret_gt_max_not_premium: list[Task],
):
    uc = UserTaskAddUsecase(uow=uow)
    with pytest.raises(MaxAmountError):
        await uc(user=fxe_user_not_premium, task_id=-1)


# pytest tests/main/challenges/task/usecases/task_user/test_user_add.py::test_user_not_premium_max_amount -v -s
@pytest.mark.asyncio
async def test_user_not_premium_max_amount(
    uow: IUnitOfWork,
    fxe_user_not_premium: User,
    mock_task_get_default: Task,
    mock_user_task_lst_ret_eq_max_not_premium: list[Task],
    mock_user_task_add: TaskUser,
):
    uc = UserTaskAddUsecase(uow=uow)
    res = await uc(user=fxe_user_not_premium, task_id=-1)
    task = res.item
    assert isinstance(task, TaskUser)


# pytest tests/main/challenges/task/usecases/task_user/test_user_add.py::test_user_premium_max_amount_error -v -s
@pytest.mark.asyncio
async def test_user_premium_max_amount_error(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_task_get_default: Task,
    mock_user_task_lst_ret_gt_max_premium: list[Task],
):
    uc = UserTaskAddUsecase(uow=uow)
    with pytest.raises(MaxAmountError):
        await uc(user=fxe_user_default, task_id=-1)


# pytest tests/main/challenges/task/usecases/task_user/test_user_add.py::test_user_premium_max_amount -v -s
@pytest.mark.asyncio
async def test_user_premium_max_amount(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_task_get_default: Task,
    mock_user_task_lst_ret_eq_max_premium: list[Task],
    mock_user_task_add: TaskUser,
):
    uc = UserTaskAddUsecase(uow=uow)
    res = await uc(user=fxe_user_default, task_id=-1)
    task = res.item
    assert isinstance(task, TaskUser)


# pytest tests/main/challenges/task/usecases/task_user/test_user_add.py::test_user_plan_premium_max_amount_error -v -s
@pytest.mark.asyncio
async def test_user_plan_premium_max_amount_error(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_task_get_default: Task,
    mock_user_task_plan_lst_ret_gt_max_premium: list[Task],
):
    uc = UserTaskAddUsecase(uow=uow)
    with pytest.raises(MaxAmountError):
        await uc(user=fxe_user_default, task_id=-1)


# pytest tests/main/challenges/task/usecases/task_user/test_user_add.py::test_user_plan_not_premium_max_amount_error -v -s
@pytest.mark.asyncio
async def test_user_plan_not_premium_max_amount_error(
    uow: IUnitOfWork,
    fxe_user_not_premium: User,
    mock_task_get_default: Task,
    mock_user_task_plan_lst_ret_gt_max_not_premium: list[Task],
):
    uc = UserTaskAddUsecase(uow=uow)
    with pytest.raises(MaxAmountError):
        await uc(user=fxe_user_not_premium, task_id=-1)


# pytest tests/main/challenges/task/usecases/task_user/test_user_add.py::test_user_plan_premium_max_amount -v -s
@pytest.mark.asyncio
async def test_user_plan_premium_max_amount(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_task_get_default: Task,
    mock_user_task_plan_lst_ret_eq_max_premium: list[Task],
    mock_user_task_add: TaskUser,
):
    uc = UserTaskAddUsecase(uow=uow)
    res = await uc(user=fxe_user_default, task_id=-1)
    task = res.item
    assert isinstance(task, TaskUser)


# pytest tests/main/challenges/task/usecases/task_user/test_user_add.py::test_user_plan_not_premium_max_amount -v -s
@pytest.mark.asyncio
async def test_user_plan_not_premium_max_amount(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_task_get_default: Task,
    mock_user_task_plan_lst_ret_eq_max_not_premium: list[Task],
    mock_user_task_add: TaskUser,
):
    uc = UserTaskAddUsecase(uow=uow)
    res = await uc(user=fxe_user_default, task_id=-1)
    task = res.item
    assert isinstance(task, TaskUser)
