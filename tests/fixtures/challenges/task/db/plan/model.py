from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.challenges.task import (
    TaskModel,
    TaskTranslateModel,
    UserTaskPlanModel,
)
from src.data.models.user.user import UserModel
from tests.fixtures.challenges.task.db.model import fxm_task_default
from tests.fixtures.user.db.model import fxm_user_default


@pytest_asyncio.fixture(scope="function")
async def fxm_task_plan_default(
    session: AsyncSession,
    fxm_user_default: UserModel,
    fxm_task_default: tuple[TaskModel, TaskTranslateModel],
) -> AsyncGenerator[UserTaskPlanModel, None]:
    task, _ = fxm_task_default
    model = UserTaskPlanModel(user_id=fxm_user_default.id, task_id=task.id)
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()
