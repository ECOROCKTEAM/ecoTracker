from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.entity.task import Task
from src.data.models.challenges.task import TaskModel, TaskTranslateModel
from src.data.repository.challenges.task import task_model_to_entity
from tests.fixtures.challenges.category.db.entity import fxe_category_default
from tests.fixtures.challenges.task.db.model import fxm_task_default, fxm_task_en


@pytest_asyncio.fixture(scope="function")
async def fxe_task_default(
    fxm_task_default: tuple[TaskModel, TaskTranslateModel],
) -> AsyncGenerator[Task, None]:
    task, translate = fxm_task_default
    yield task_model_to_entity(task, translate)


@pytest_asyncio.fixture(scope="function")
async def fxe_task_en(
    fxm_task_en: tuple[TaskModel, TaskTranslateModel],
) -> AsyncGenerator[Task, None]:
    task, translate = fxm_task_en
    yield task_model_to_entity(task, translate)
