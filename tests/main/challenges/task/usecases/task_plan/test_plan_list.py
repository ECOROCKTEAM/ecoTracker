import pytest

from src.core.dto.mock import MockObj
from src.core.entity.task import TaskUserPlan
from src.core.entity.user import User
from src.core.interfaces.repository.challenges.task import TaskUserPlanFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_user_plan_list import (
    UserTaskPlanListUsecase,
)
from tests.fixtures.challenges.task.usecase.user_task import (
    mock_user_task_plan_check_filter,
)
from tests.fixtures.const import (
    DEFAULT_TEST_USECASE_TASK_ID,
    DEFAULT_TEST_USECASE_USER_ID,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/challenges/task/usecases/task_plan/test_plan_list.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_user_task_plan_check_filter: list[TaskUserPlan],
):
    uc = UserTaskPlanListUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        filter_obj=TaskUserPlanFilter(task_active=True),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    plans = res.item
    assert isinstance(plans, list)
    assert len(plans) == 1
    plan = plans[0]
    assert isinstance(plan, TaskUserPlan)
    assert plan.task_id == DEFAULT_TEST_USECASE_TASK_ID
    assert plan.user_id == DEFAULT_TEST_USECASE_USER_ID
