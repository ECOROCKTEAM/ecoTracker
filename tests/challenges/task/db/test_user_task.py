from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.task import TaskUserCreateDTO, TaskUserUpdateDTO
from src.core.dto.mock import MockObj
from src.core.entity.task import Task, TaskUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.challenges.task import TaskUserFilter
from src.data.models.challenges.task import UserTaskModel
from src.data.models.user.user import UserModel
from src.data.repository.challenges.task import IRepositoryTask, RepositoryTask
from tests.fixtures.challenges.category.db.model import fxm_category_default
from tests.fixtures.challenges.task.db.entity import fxe_task_default
from tests.fixtures.challenges.task.db.model import fxm_task_default
from tests.fixtures.challenges.task.db.user.entity import fxe_user_task_default
from tests.fixtures.challenges.task.db.user.model import fxm_user_task_default
from tests.fixtures.user.db.entity import fxe_user_default
from tests.fixtures.user.db.model import fxm_user_default


# python -m pytest tests/challenges/task/db/test_user_task.py::test_get_user_task_ok -v -s
@pytest.mark.asyncio
async def test_get_user_task_ok(repo: IRepositoryTask, fxe_user_task_default: TaskUser):
    task = await repo.user_task_get(id=fxe_user_task_default.id)
    assert fxe_user_task_default.id == task.id
    assert fxe_user_task_default.user_id == task.user_id
    assert fxe_user_task_default.task_id == task.task_id
    assert fxe_user_task_default.date_start == task.date_start
    assert fxe_user_task_default.date_close == task.date_close
    assert fxe_user_task_default.status == task.status


# python -m pytest tests/challenges/task/db/test_user_task.py::test_get_user_task_not_found -v -s
@pytest.mark.asyncio
async def test_get_user_task_not_found(repo: IRepositoryTask):
    with pytest.raises(EntityNotFound):
        _ = await repo.user_task_get(id=-1)


# python -m pytest tests/challenges/task/db/test_user_task.py::test_create_user_task_ok -v -s
@pytest.mark.asyncio
async def test_create_user_task_ok(
    session: AsyncSession, repo: IRepositoryTask, fxe_user_default: User, fxe_task_default: Task
):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    user_task_list = await repo.user_task_lst(user_id=fxe_user_default.id, filter_obj=TaskUserFilter(), **default_kw)
    assert len(user_task_list) == 0
    user_task = await repo.user_task_add(
        user_id=fxe_user_default.id,
        obj=TaskUserCreateDTO(
            task_id=fxe_task_default.id,
        ),
    )
    await session.commit()
    assert user_task.id is not None
    assert user_task.user_id == fxe_user_default.id
    assert user_task.task_id == fxe_task_default.id
    assert isinstance(user_task.date_start, datetime)
    assert user_task.date_close is None
    assert user_task.status == OccupancyStatusEnum.ACTIVE

    user_task_list = await repo.user_task_lst(user_id=fxe_user_default.id, filter_obj=TaskUserFilter(), **default_kw)
    assert len(user_task_list) == 1

    create_model = await session.get(entity=UserTaskModel, ident={"id": user_task.id})
    assert isinstance(create_model, UserTaskModel)
    await session.delete(create_model)
    await session.commit()


# python -m pytest tests/challenges/task/db/test_user_task.py::test_create_user_task_not_created -v -s
@pytest.mark.asyncio
async def test_create_user_task_not_created(
    session: AsyncSession, repo: IRepositoryTask, fxe_user_default: User, fxe_task_default: Task
):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    user_task_list = await repo.user_task_lst(user_id=fxe_user_default.id, filter_obj=TaskUserFilter(), **default_kw)
    assert len(user_task_list) == 0
    with pytest.raises(EntityNotCreated):
        _ = await repo.user_task_add(
            user_id=-1,
            obj=TaskUserCreateDTO(
                task_id=fxe_task_default.id,
            ),
        )
    await session.rollback()
    user_task_list = await repo.user_task_lst(user_id=fxe_user_default.id, filter_obj=TaskUserFilter(), **default_kw)
    assert len(user_task_list) == 0


# python -m pytest tests/challenges/task/db/test_user_task.py::test_update_user_task -v -s
@pytest.mark.asyncio
async def test_update_user_task(
    session: AsyncSession,
    repo: IRepositoryTask,
    fxe_user_task_default: TaskUser,
):
    assert fxe_user_task_default.status == OccupancyStatusEnum.ACTIVE
    assert fxe_user_task_default.date_close is None

    updated = await repo.user_task_update(
        id=fxe_user_task_default.id,
        obj=TaskUserUpdateDTO(status=OccupancyStatusEnum.FINISH),
    )
    await session.commit()

    assert isinstance(updated.date_close, datetime)
    assert updated.status == OccupancyStatusEnum.FINISH

    date_after_update = updated.date_close

    updated_second = await repo.user_task_update(
        id=fxe_user_task_default.id,
        obj=TaskUserUpdateDTO(status=OccupancyStatusEnum.REJECT),
    )
    await session.commit()

    assert isinstance(updated_second.date_close, datetime)
    assert updated_second.status == OccupancyStatusEnum.REJECT
    assert updated_second.date_close > date_after_update


# python -m pytest tests/challenges/task/db/test_user_task.py::test_update_user_task_not_found -v -s
@pytest.mark.asyncio
async def test_update_user_task_not_found(
    repo: IRepositoryTask,
    fxe_user_task_default: TaskUser,
):
    with pytest.raises(EntityNotFound):
        _ = await repo.user_task_update(id=-1, obj=TaskUserUpdateDTO(status=OccupancyStatusEnum.FINISH))


# python -m pytest tests/challenges/task/db/test_user_task.py::test_user_task_lst -v -s
@pytest.mark.asyncio
async def test_user_task_lst(repo: IRepositoryTask, fxe_user_task_default: TaskUser):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    user_task_list = await repo.user_task_lst(
        user_id=fxe_user_task_default.user_id,
        filter_obj=TaskUserFilter(
            task_id=fxe_user_task_default.task_id, task_active=True, status=OccupancyStatusEnum.ACTIVE
        ),
        **default_kw,
    )
    assert len(user_task_list) == 1

    user_task = user_task_list[0]

    assert user_task.id is not None
    assert user_task.user_id == fxe_user_task_default.user_id
    assert user_task.task_id == fxe_user_task_default.task_id
    assert user_task.status == OccupancyStatusEnum.ACTIVE

    user_task_list = await repo.user_task_lst(
        user_id=fxe_user_task_default.user_id, filter_obj=TaskUserFilter(), **default_kw
    )
    assert len(user_task_list) == 1

    user_task_list = await repo.user_task_lst(
        user_id=fxe_user_task_default.user_id, filter_obj=TaskUserFilter(task_id=-1), **default_kw
    )
    assert len(user_task_list) == 0

    user_task_list = await repo.user_task_lst(
        user_id=fxe_user_task_default.user_id,
        filter_obj=TaskUserFilter(status=OccupancyStatusEnum.FINISH),
        **default_kw,
    )
    assert len(user_task_list) == 0

    user_task_list = await repo.user_task_lst(
        user_id=fxe_user_task_default.user_id,
        filter_obj=TaskUserFilter(task_active=False),
        **default_kw,
    )
    assert len(user_task_list) == 0
