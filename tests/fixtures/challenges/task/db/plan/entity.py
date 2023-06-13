from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.entity.task import TaskUserPlan
from src.data.models.challenges.task import UserTaskPlanModel
from src.data.repository.challenges.task import plan_model_to_entity
from tests.fixtures.challenges.task.db.plan.model import fxm_task_plan_default


@pytest_asyncio.fixture(scope="function")
async def fxe_task_plan_default(
    fxm_task_plan_default: UserTaskPlanModel,
) -> AsyncGenerator[TaskUserPlan, None]:
    yield plan_model_to_entity(fxm_task_plan_default)
