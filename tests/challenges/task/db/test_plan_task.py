import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.task import TaskUserPlanCreateDTO
from src.core.dto.mock import MockObj
from src.core.entity.task import Task, TaskUserPlan
from src.core.entity.user import User
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.task import (
    TaskFilter,
    TaskUserPlanFilter,
)
from src.data.models.challenges.task import UserTaskPlanModel
from src.data.repository.challenges.task import IRepositoryTask
from tests.fixtures.challenges.category.db.model import fxm_category_default
from tests.fixtures.challenges.task.db.entity import fxe_task_default
from tests.fixtures.challenges.task.db.model import fxm_task_default
from tests.fixtures.challenges.task.db.plan.entity import fxe_task_plan_default
from tests.fixtures.challenges.task.db.plan.model import fxm_task_plan_default
from tests.fixtures.user.db.entity import fxe_user_default
from tests.fixtures.user.db.model import fxm_user_default


# python -m pytest tests/challenges/task/db/test_plan_task.py::test_plan_list -v -s
@pytest.mark.asyncio
async def test_plan_list(repo: IRepositoryTask, fxe_task_plan_default: UserTaskPlanModel):
    default_kw = dict(order_obj=MockObj(), pagination_obj=MockObj())
    plan_list = await repo.plan_lst(
        user_id=fxe_task_plan_default.user_id, filter_obj=TaskUserPlanFilter(task_active=True), **default_kw
    )
    assert len(plan_list) == 1
    plan = plan_list[0]
    assert isinstance(plan, TaskUserPlan)
    assert fxe_task_plan_default.user_id == plan.user_id
    assert fxe_task_plan_default.task_id == plan.task_id

    plan_list = await repo.plan_lst(
        user_id=fxe_task_plan_default.user_id, filter_obj=TaskUserPlanFilter(task_active=False), **default_kw
    )
    assert len(plan_list) == 0


# python -m pytest tests/challenges/task/db/test_plan_task.py::test_plan_create -v -s
@pytest.mark.asyncio
async def test_plan_create(
    session: AsyncSession,
    repo: IRepositoryTask,
    fxe_task_default: Task,
    fxe_user_default: User,
):
    plan = await repo.plan_create(
        obj=TaskUserPlanCreateDTO(
            user_id=fxe_user_default.id,
            task_id=fxe_task_default.id,
        )
    )
    assert isinstance(plan, TaskUserPlan)
    assert plan.user_id == fxe_user_default.id
    assert plan.task_id == fxe_task_default.id

    default_kw = dict(order_obj=MockObj(), pagination_obj=MockObj())
    plan_list = await repo.plan_lst(user_id=plan.user_id, filter_obj=TaskUserPlanFilter(task_active=True), **default_kw)
    assert len(plan_list) == 1

    create_model = await session.get(entity=UserTaskPlanModel, ident={"user_id": plan.user_id, "task_id": plan.task_id})
    assert isinstance(create_model, UserTaskPlanModel)
    await session.delete(create_model)
    await session.commit()


# python -m pytest tests/challenges/task/db/test_plan_task.py::test_not_created -v -s
@pytest.mark.asyncio
async def test_plan_not_created(
    session: AsyncSession,
    repo: IRepositoryTask,
    fxe_task_default: Task,
    fxe_user_default: User,
):
    default_kw = dict(order_obj=MockObj(), pagination_obj=MockObj())
    plan_list = await repo.plan_lst(
        user_id=fxe_user_default.id, filter_obj=TaskUserPlanFilter(task_active=True), **default_kw
    )
    assert len(plan_list) == 0

    with pytest.raises(EntityNotCreated):
        _ = await repo.plan_create(
            obj=TaskUserPlanCreateDTO(
                user_id=-1,
                task_id=fxe_task_default.id,
            )
        )
    await session.rollback()
    with pytest.raises(EntityNotCreated):
        _ = await repo.plan_create(
            obj=TaskUserPlanCreateDTO(
                user_id=fxe_user_default.id,
                task_id=-1,
            )
        )
    await session.rollback()

    plan_list = await repo.plan_lst(user_id=fxe_user_default.id, filter_obj=TaskUserPlanFilter(), **default_kw)
    assert len(plan_list) == 0


# python -m pytest tests/challenges/task/db/test_plan_task.py::test_plan_delete -v -s
@pytest.mark.asyncio
async def test_plan_delete(
    session: AsyncSession,
    repo: IRepositoryTask,
    fxe_task_default: Task,
    fxe_user_default: User,
):
    default_kw = dict(order_obj=MockObj(), pagination_obj=MockObj())

    plan = await repo.plan_create(
        obj=TaskUserPlanCreateDTO(
            user_id=fxe_user_default.id,
            task_id=fxe_task_default.id,
        )
    )
    assert plan.user_id == fxe_user_default.id
    assert plan.task_id == fxe_task_default.id
    await session.commit()

    plan_list = await repo.plan_lst(user_id=fxe_user_default.id, filter_obj=TaskUserPlanFilter(), **default_kw)
    assert len(plan_list) == 1

    deleted_plan = await repo.plan_delete(
        user_id=fxe_user_default.id,
        task_id=fxe_task_default.id,
    )
    assert isinstance(deleted_plan, TaskUserPlan)
    await session.commit()

    plan_list = await repo.plan_lst(user_id=fxe_user_default.id, filter_obj=TaskUserPlanFilter(), **default_kw)
    assert len(plan_list) == 0


# python -m pytest tests/challenges/task/db/test_plan_task.py::test_plan_not_delete -v -s
@pytest.mark.asyncio
async def test_plan_not_delete(
    session: AsyncSession,
    repo: IRepositoryTask,
    fxe_task_default: Task,
    fxe_user_default: User,
):
    default_kw = dict(order_obj=MockObj(), pagination_obj=MockObj())
    plan_list = await repo.plan_lst(
        user_id=fxe_user_default.id, filter_obj=TaskUserPlanFilter(task_active=True), **default_kw
    )
    assert len(plan_list) == 0

    with pytest.raises(EntityNotFound):
        _ = await repo.plan_delete(
            user_id=fxe_user_default.id,
            task_id=fxe_task_default.id,
        )
