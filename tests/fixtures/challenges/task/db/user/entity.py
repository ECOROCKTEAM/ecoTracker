from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.entity.task import TaskUser
from src.data.models.challenges.task import UserTaskModel
from src.data.repository.challenges.task import user_task_to_entity
from tests.fixtures.challenges.category.db.entity import fxe_category_default
from tests.fixtures.challenges.task.db.model import fxm_task_default, fxm_task_en


@pytest_asyncio.fixture(scope="function")
async def fxe_user_task_default(
    fxm_user_task_default: UserTaskModel,
) -> AsyncGenerator[TaskUser, None]:
    yield user_task_to_entity(fxm_user_task_default)
