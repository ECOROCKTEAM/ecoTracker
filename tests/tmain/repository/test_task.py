import random
from datetime import datetime
from random import choice

import pytest
from pyparsing import Optional

from src import data
from src.core.const.translate import DEFAULT_LANGUANGE
from src.core.dto.challenges.task import (
    TaskUserCreateDTO,
    TaskUserPlanCreateDTO,
    TaskUserUpdateDTO,
)
from src.core.dto.utils import IterableObj, SortObj
from src.core.entity.task import Task, TaskUserPlan
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum
from src.core.exception.base import (
    EntityNotChange,
    EntityNotCreated,
    EntityNotFound,
    TranslateNotFound,
)
from src.core.interfaces.repository.challenges.task import (
    IRepositoryTask,
    SortUserTaskObj,
    TaskFilter,
    TaskUserFilter,
    TaskUserPlanFilter,
)
from src.data.models.challenges.task import TaskModel
from src.data.models.user.user import UserModel
from tests.dataloader import dataloader


# pytest tests/tmain/repository/test_task.py::test_get_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "language_list", [[LanguageEnum.FR, LanguageEnum.EN], [LanguageEnum.EN], [LanguageEnum.RU, LanguageEnum.EN]]
)
async def test_get_ok(dl: dataloader, repo_task: IRepositoryTask, language_list: list[LanguageEnum]):
    # Arrange
    asrt_task = await dl.create_task(language_list=language_list)
    await dl.create_task_list_random()

    # Act && Assert
    for lang in language_list:
        task = await repo_task.get(id=asrt_task.id, lang=lang)

        assert asrt_task.id == task.id
        assert lang == task.language


# pytest tests/tmain/repository/test_task.py::test_get_default_language -v -s
@pytest.mark.asyncio
async def test_get_default_language(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    # Create RU and default language (EN) and we will get FR language, but we must be get EN by default
    asrt_task = await dl.create_task(language_list=[LanguageEnum.RU, LanguageEnum.EN])
    language_not_exist = LanguageEnum.FR
    language_asrt = LanguageEnum.EN

    # Act
    task = await repo_task.get(id=asrt_task.id, lang=language_not_exist)

    # Assert
    assert asrt_task.id == task.id
    assert language_asrt == task.language


# pytest tests/tmain/repository/test_task.py::test_get_language_not_found_error -v -s
@pytest.mark.asyncio
async def test_get_language_not_found_error(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    # Create only RU, not created default language (EN) and we will get FR language
    task = await dl.create_task(language_list=[LanguageEnum.RU])
    language_not_exist = LanguageEnum.FR

    # Act
    with pytest.raises(TranslateNotFound) as e:
        await repo_task.get(id=task.id, lang=language_not_exist)

    # Assert
    assert f"with task_translate=None" in str(e.value)


# pytest tests/tmain/repository/test_task.py::test_get_task_not_found_error -v -s
@pytest.mark.asyncio
async def test_get_task_not_found_error(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    await dl.create_task_list_random()
    not_exist_id = -1

    # Act
    with pytest.raises(EntityNotFound) as e:
        await repo_task.get(id=not_exist_id, lang=DEFAULT_LANGUANGE)

    # Assert
    assert f"Task.id={not_exist_id} not found" in str(e.value)


async def _arrange_lst_fltr_empty(dl: dataloader) -> tuple[TaskFilter, int]:
    fltr = TaskFilter()
    category_list = await dl.create_category_list_random(count=4)
    task_list = await dl.create_task_list_random(count=20, category_list=category_list)
    return fltr, len(task_list)


async def _arrange_lst_fltr_active(dl: dataloader) -> tuple[TaskFilter, int]:
    fltr = TaskFilter(active=True)
    await dl.create_task(active=True)
    await dl.create_task(active=True)
    await dl.create_task(active=False)
    await dl.create_task(active=True)
    return fltr, 3


async def _arrange_lst_fltr_category(dl: dataloader) -> tuple[TaskFilter, int]:
    category_list = await dl.create_category_list_random(count=4)
    task_list = await dl.create_task_list_random(count=20, category_list=category_list)
    category = random.choice(category_list)
    cnt = len([task for task in task_list if task.category_id == category.id])
    fltr = TaskFilter(category_id=category.id)
    await dl.create_task(active=True)
    await dl.create_task(active=True)
    await dl.create_task(active=False)
    await dl.create_task(active=True)
    return fltr, cnt


# pytest tests/tmain/repository/test_task.py::test_lst_fltr -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrage_func", [_arrange_lst_fltr_empty, _arrange_lst_fltr_active, _arrange_lst_fltr_category])
async def test_lst_fltr(dl: dataloader, repo_task: IRepositoryTask, arrage_func):
    keys = list(TaskFilter.__dataclass_fields__.keys())
    assert len(keys) == 2

    # Arrange
    fltr, asrt_count = await arrage_func(dl=dl)

    # Act
    task_list = await repo_task.lst(
        filter_obj=fltr, sorting_obj=SortObj(), iterable_obj=IterableObj(), lang=LanguageEnum.EN
    )

    # Assert
    assert asrt_count == len(task_list.items)
    assert asrt_count == task_list.total


async def _arrange_lst_pagination_limit_none_offset_zero(dl: dataloader) -> tuple[int, int, int | None, int]:
    await dl.create_task_list_random(count=20)
    return 20, 20, None, 0


async def _arrange_lst_pagination_limit_5_offset_zero(dl: dataloader) -> tuple[int, int, int | None, int]:
    await dl.create_task_list_random(count=20)
    return 20, 5, 5, 0


async def _arrange_lst_pagination_limit_5_offset_5(dl: dataloader) -> tuple[int, int, int | None, int]:
    await dl.create_task_list_random(count=20)
    return 20, 5, 5, 5


async def _arrange_lst_pagination_limit_none_offset_19(dl: dataloader) -> tuple[int, int, int | None, int]:
    await dl.create_task_list_random(count=20)
    return 20, 1, None, 19


# pytest tests/tmain/repository/test_task.py::test_lst_pagination -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrage_func",
    [
        _arrange_lst_pagination_limit_none_offset_zero,
        _arrange_lst_pagination_limit_5_offset_zero,
        _arrange_lst_pagination_limit_5_offset_5,
        _arrange_lst_pagination_limit_none_offset_19,
    ],
)
async def test_lst_pagination(dl: dataloader, repo_task: IRepositoryTask, arrage_func):
    # Arrange
    asrt_total, asrt_count, asrt_limit, asrt_offset = await arrage_func(dl=dl)

    # Act
    task_list = await repo_task.lst(
        filter_obj=TaskFilter(),
        sorting_obj=SortObj(),
        iterable_obj=IterableObj(limit=asrt_limit, offset=asrt_offset),
        lang=LanguageEnum.EN,
    )

    # Assert
    assert asrt_count == len(task_list.items)
    assert asrt_total == task_list.total
    assert asrt_limit == task_list.limit
    assert asrt_offset == task_list.offset


# pytest tests/tmain/repository/test_task.py::test_user_task_add_ok -v -s
@pytest.mark.asyncio
async def test_user_task_add_ok(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    asrt_user = await dl.user_loader.create()
    asrt_task = await dl.create_task()

    # Act
    user_task_add = await repo_task.user_task_add(user_id=asrt_user.id, obj=TaskUserCreateDTO(task_id=asrt_task.id))

    # Assert
    assert user_task_add.task_id == asrt_task.id
    assert user_task_add.user_id == asrt_user.id
    assert user_task_add.status == OccupancyStatusEnum.ACTIVE
    assert isinstance(user_task_add.date_start, datetime)
    assert user_task_add.date_close is None


# pytest tests/tmain/repository/test_task.py::test_user_task_add_not_created_error -v -s
@pytest.mark.asyncio
async def test_user_task_add_not_created_error(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    user = await dl.user_loader.create()
    not_exist_id = -1

    # Act && Assert
    with pytest.raises(EntityNotCreated) as e:
        await repo_task.user_task_add(user_id=user.id, obj=TaskUserCreateDTO(task_id=not_exist_id))
    assert "Not found fk" in str(e.value)


# pytest tests/tmain/repository/test_task.py::test_user_task_get_ok -v -s
@pytest.mark.asyncio
async def test_user_task_get_ok(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    user = await dl.user_loader.create()
    asrt_user_task = await dl.create_user_task(user=user, status=OccupancyStatusEnum.ACTIVE)
    await dl.create_user_task(user=user)

    # Act
    user_task = await repo_task.user_task_get(user_id=user.id, id=asrt_user_task.id)

    # Assert

    assert user_task.id == asrt_user_task.id
    assert user_task.task_id == asrt_user_task.task_id
    assert user_task.user_id == asrt_user_task.user_id == user.id
    assert isinstance(user_task.status, OccupancyStatusEnum)
    assert user_task.status == asrt_user_task.status == OccupancyStatusEnum.ACTIVE
    assert user_task.date_start == asrt_user_task.date_start
    assert isinstance(user_task.date_start, datetime)
    assert user_task.date_close is None
    assert user_task.date_close == asrt_user_task.date_close


# pytest tests/tmain/repository/test_task.py::test_user_task_get_not_found_error -v -s
@pytest.mark.asyncio
async def test_user_task_get_not_found_error(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    user = await dl.user_loader.create()
    await dl.create_user_task(user=user)
    await dl.create_user_task(user=user)
    not_exist_id = -1

    # Act
    with pytest.raises(EntityNotFound) as e:
        await repo_task.user_task_get(user_id=user.id, id=not_exist_id)

    #     # Assert
    assert f"UserTask object with id={not_exist_id} not found" in str(e.value)


# pytest tests/tmain/repository/test_task.py::test_user_task_update_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "obj",
    [
        TaskUserUpdateDTO(status=OccupancyStatusEnum.FINISH),
        TaskUserUpdateDTO(status=OccupancyStatusEnum.REJECT),
        TaskUserUpdateDTO(status=OccupancyStatusEnum.OVERDUE),
    ],
)
async def test_user_task_update_ok(dl: dataloader, repo_task: IRepositoryTask, obj: TaskUserUpdateDTO):
    keys = [key for key, f in TaskUserUpdateDTO.__dataclass_fields__.items() if f.init is True]
    assert len(keys) == 1

    # Arrange
    user = await dl.user_loader.create()
    asrt_user_task = await dl.create_user_task(user=user, status=OccupancyStatusEnum.ACTIVE)
    created_status = asrt_user_task.status
    created_date_start = asrt_user_task.date_start
    created_date_close = asrt_user_task.date_close

    # Act
    task_update = await repo_task.user_task_update(user_id=user.id, id=asrt_user_task.id, obj=obj)

    # Assert
    assert asrt_user_task.id == task_update.id
    assert asrt_user_task.task_id == task_update.task_id
    assert created_status != task_update.status
    assert created_date_start == task_update.date_start
    assert created_date_close != task_update.date_start
    assert isinstance(task_update.date_close, datetime)


# pytest tests/tmain/repository/test_task.py::test_user_task_update_empty_fail -v -s
@pytest.mark.asyncio
async def test_user_task_update_empty_fail(
    dl: dataloader,
    repo_task: IRepositoryTask,
):
    # Arrange
    user = await dl.user_loader.create()
    asrt_user_task = await dl.create_user_task(user=user, status=OccupancyStatusEnum.ACTIVE)

    # Act && Assert
    with pytest.raises(EntityNotChange) as e:
        await repo_task.user_task_update(user_id=user.id, id=asrt_user_task.id, obj=TaskUserUpdateDTO())

    assert "Empty data for update" in str(e.value)


# pytest tests/tmain/repository/test_task.py::test_user_plan_create_empty_fail -v -s
@pytest.mark.asyncio
async def test_user_plan_create_empty_fail(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    user = await dl.user_loader.create()
    task_id_not_exist = -1

    obj = TaskUserPlanCreateDTO(user_id=user.id, task_id=task_id_not_exist)

    # Act
    with pytest.raises(EntityNotCreated) as e:
        await repo_task.plan_create(obj=obj)

    # Assert
    assert "Not found fk" in str(e.value)


# pytest tests/tmain/repository/test_task.py::test_user_plan_create_ok -v -s
@pytest.mark.asyncio
async def test_user_plan_create_ok(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    user = await dl.user_loader.create()
    task = await dl.create_task()
    await dl.create_task_list_random()

    obj = TaskUserPlanCreateDTO(user_id=user.id, task_id=task.id)

    # Act
    user_task_plan = await repo_task.plan_create(obj=obj)

    # Assert
    assert user.id == user_task_plan.user_id
    assert task.id == user_task_plan.task_id


# pytest tests/tmain/repository/test_task.py::test_user_plan_delete_ok -v -s
@pytest.mark.asyncio
async def test_user_plan_delete_ok(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    user = await dl.user_loader.create()
    task = await dl.create_task()
    await dl.create_user_task_plan(user=user, task=task)
    await dl.create_task_list_random()

    # Act
    user_task_plan_delete = await repo_task.plan_delete(user_id=user.id, task_id=task.id)

    # Assert
    assert user_task_plan_delete.task_id == task.id
    assert user_task_plan_delete.user_id == user.id


# pytest tests/tmain/repository/test_task.py::test_user_task_plan_delete_task_not_found_error -v -s
@pytest.mark.asyncio
async def test_user_task_plan_delete_task_not_found_error(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    user = await dl.user_loader.create()
    task_id_not_exist = -1

    # Act
    with pytest.raises(EntityNotFound) as e:
        await repo_task.plan_delete(user_id=user.id, task_id=task_id_not_exist)

    # Assert
    assert f"UserTaskPlan with task_id={task_id_not_exist}, user_id={user.id} not deleted" in str(e.value)


async def _arrange_user_task_lst_offset_15_pagination_limit_5(
    dl: dataloader, user: UserModel
) -> tuple[int, int, int, int | None]:
    await dl.create_user_task_list(user=user, count=20)
    return 20, 5, 15, 5


async def _arrange_user_task_lst_offset_0_pagination_limit_none(
    dl: dataloader, user: UserModel
) -> tuple[int, int, int, int | None]:
    await dl.create_user_task_list(user=user, count=20)
    return 20, 20, 0, None


async def _arrange_user_task_lst_offset_17_pagination_limit_none(
    dl: dataloader, user: UserModel
) -> tuple[int, int, int, int | None]:
    await dl.create_user_task_list(user=user, count=20)
    return 20, 3, 17, None


async def _arrange_user_task_lst_offset_5_pagination_limit_5(
    dl: dataloader, user: UserModel
) -> tuple[int, int, int, int | None]:
    await dl.create_user_task_list(user=user, count=20)
    return 20, 5, 0, 5


# pytest tests/tmain/repository/test_task.py::test_user_task_list_pagination -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [
        _arrange_user_task_lst_offset_15_pagination_limit_5,
        _arrange_user_task_lst_offset_17_pagination_limit_none,
        _arrange_user_task_lst_offset_0_pagination_limit_none,
        _arrange_user_task_lst_offset_5_pagination_limit_5,
    ],
)
async def test_user_task_list_pagination(dl: dataloader, repo_task: IRepositoryTask, arrange_func):
    # Arrange
    user = await dl.user_loader.create()
    asrt_total, asrt_count, asrt_offset, asrt_limit = await arrange_func(dl=dl, user=user)

    # Act
    user_task_list = await repo_task.user_task_lst(
        user_id=user.id,
        filter_obj=TaskUserFilter(),
        sorting_obj=SortUserTaskObj(),
        iterable_obj=IterableObj(limit=asrt_limit, offset=asrt_offset),
    )

    # Assert
    assert asrt_count == len(user_task_list.items)
    assert asrt_total == user_task_list.total
    assert asrt_limit == user_task_list.limit
    assert asrt_offset == user_task_list.offset


async def _arrange_user_task_plan_list_offset_5_pagination_limit_3(
    dl: dataloader, user: UserModel
) -> tuple[int, int, int, int | None]:
    await dl.create_user_task_plan_list(user=user, count=20)
    return 20, 3, 5, 3


async def _arrange_user_task_plan_list_offset_0_pagination_limit_none(
    dl: dataloader, user: UserModel
) -> tuple[int, int, int, int | None]:
    await dl.create_user_task_plan_list(user=user, count=20)
    return 20, 20, 0, None


async def _arrange_user_task_plan_list_offset_18_pagination_limit_none(
    dl: dataloader, user: UserModel
) -> tuple[int, int, int, int | None]:
    await dl.create_user_task_plan_list(user=user, count=20)
    return 20, 2, 18, None


async def _arrange_user_task_plan_list_offset_0_pagination_limit_10(
    dl: dataloader, user: UserModel
) -> tuple[int, int, int, int | None]:
    await dl.create_user_task_plan_list(user=user, count=20)
    return 20, 10, 0, 10


# pytest tests/tmain/repository/test_task.py::test_user_plan_list_pagination -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [
        _arrange_user_task_plan_list_offset_5_pagination_limit_3,
        _arrange_user_task_plan_list_offset_0_pagination_limit_none,
        _arrange_user_task_plan_list_offset_18_pagination_limit_none,
        _arrange_user_task_plan_list_offset_0_pagination_limit_10,
    ],
)
async def test_user_plan_list_pagination(dl: dataloader, repo_task: IRepositoryTask, arrange_func):
    # Arrange
    user = await dl.user_loader.create()
    asrt_total, asrt_count, asrt_offset, asrt_limit = await arrange_func(dl=dl, user=user)

    # Act
    user_task_plan_list = await repo_task.plan_lst(
        user_id=user.id,
        filter_obj=TaskUserPlanFilter(),
        sorting_obj=SortUserTaskObj(),
        iterable_obj=IterableObj(limit=asrt_limit, offset=asrt_offset),
    )

    # Assert
    assert asrt_total == user_task_plan_list.total
    assert asrt_count == len(user_task_plan_list.items)
    assert asrt_limit == user_task_plan_list.limit
    assert asrt_offset == user_task_plan_list.offset


async def _arrange_user_task_list_filter_task_id(
    dl: dataloader, user: UserModel
) -> tuple[int, TaskUserFilter, TaskModel]:
    task = await dl.create_task()
    task_not_in_filter = await dl.create_task()

    await dl.create_user_task(user=user, task=task)
    await dl.create_user_task(user=user, task=task)
    await dl.create_user_task(user=user, task=task)
    await dl.create_user_task(user=user, task=task_not_in_filter)
    filter_obj = TaskUserFilter(task_id=task.id)
    total = 3
    return total, filter_obj, task


async def _arrange_user_task_list_filter_task_active(
    dl: dataloader, user: UserModel
) -> tuple[int, TaskUserFilter, TaskModel]:
    task_active = await dl.create_task(active=True)
    task_not_active = await dl.create_task(active=False)

    await dl.create_user_task(user=user, task=task_active)
    await dl.create_user_task(user=user, task=task_active)
    await dl.create_user_task(user=user, task=task_not_active)
    await dl.create_user_task(user=user, task=task_not_active)
    filter_obj = TaskUserFilter(task_active=True)
    total = 2
    return total, filter_obj, task_active


async def _arrange_user_task_list_filter_status(
    dl: dataloader, user: UserModel
) -> tuple[int, TaskUserFilter, TaskModel]:
    task = await dl.create_task()

    await dl.create_user_task(user=user, task=task, status=OccupancyStatusEnum.ACTIVE)
    await dl.create_user_task(user=user, task=task, status=OccupancyStatusEnum.ACTIVE)
    await dl.create_user_task(user=user, task=task, status=OccupancyStatusEnum.REJECT)
    await dl.create_user_task(user=user, task=task, status=OccupancyStatusEnum.FINISH)
    await dl.create_user_task(user=user, task=task, status=OccupancyStatusEnum.OVERDUE)
    total = 2
    filter_obj = TaskUserFilter(status=OccupancyStatusEnum.ACTIVE)
    return total, filter_obj, task


# pytest tests/tmain/repository/test_task.py::test_user_task_list_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [
        _arrange_user_task_list_filter_task_id,
        _arrange_user_task_list_filter_task_active,
        _arrange_user_task_list_filter_status,
    ],
)
async def test_user_task_list_ok(dl: dataloader, repo_task: IRepositoryTask, arrange_func):
    # Arrange
    user = await dl.user_loader.create()
    total, asrt_filter_obj, task = await arrange_func(dl=dl, user=user)

    # Act
    user_task_list = await repo_task.user_task_lst(
        user_id=user.id, filter_obj=asrt_filter_obj, sorting_obj=SortUserTaskObj(), iterable_obj=IterableObj()
    )

    user_id_set = {user_task.user_id for user_task in user_task_list.items}
    task_id_set = {user_task.task_id for user_task in user_task_list.items}
    user_tasks_status_set = {user_task.status for user_task in user_task_list.items}

    # Asser
    assert len(user_task_list.items) == total
    assert user_id_set == set([user.id])
    assert task_id_set == set([task.id])
    assert all([isinstance(user_task.date_start, datetime) for user_task in user_task_list.items])

    if asrt_filter_obj.status is not None:
        assert set([asrt_filter_obj.status]) == user_tasks_status_set
    if asrt_filter_obj.task_id is not None:
        assert set([asrt_filter_obj.task_id]) == task_id_set
    if asrt_filter_obj.task_active is not None:
        for id in task_id_set:
            task = await dl.task_loader.get(id=id)
            assert isinstance(task, TaskModel)
            assert asrt_filter_obj.task_active == task.active


async def _arrange_user_task_plan_list_filter_task_active(
    dl: dataloader, user: UserModel
) -> tuple[int, TaskUserPlanFilter, list[TaskModel]]:
    task_active_1 = await dl.create_task()
    task_active_2 = await dl.create_task()

    task_not_active_1 = await dl.create_task(active=False)

    await dl.create_user_task_plan(user=user, task=task_active_1)
    await dl.create_user_task_plan(user=user, task=task_active_2)
    await dl.create_user_task_plan(user=user, task=task_not_active_1)

    filtered_task_list = [task_active_1, task_active_2]
    total = 2
    filter_obj = TaskUserPlanFilter(task_active=True)
    return total, filter_obj, filtered_task_list


async def _arrange_user_task_plan_list_filter_category_id(
    dl: dataloader, user: UserModel
) -> tuple[int, TaskUserPlanFilter, list[TaskModel]]:
    category = await dl.create_category()
    fake_category = await dl.create_category()

    task_1 = await dl.create_task(category=category)
    task_2 = await dl.create_task(category=category)
    task_3 = await dl.create_task(category=category)
    fake_task = await dl.create_task(category=fake_category)

    await dl.create_user_task_plan(user=user, task=task_1)
    await dl.create_user_task_plan(user=user, task=task_2)
    await dl.create_user_task_plan(user=user, task=task_3)
    await dl.create_user_task_plan(user=user, task=fake_task)

    filtered_task_list = [task_1, task_2, task_3]
    total = 3
    filter_obj = TaskUserPlanFilter(category_id=category.id)
    return total, filter_obj, filtered_task_list


# pytest tests/tmain/repository/test_task.py::test_user_task_plan_list_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func", [_arrange_user_task_plan_list_filter_task_active, _arrange_user_task_plan_list_filter_category_id]
)
async def test_user_task_plan_list_ok(dl: dataloader, repo_task: IRepositoryTask, arrange_func):
    # Arrange
    user = await dl.user_loader.create()
    await dl.user_loader.create()

    total, filter_obj, filtered_task_list = await arrange_func(dl=dl, user=user)

    asrt_task_set_id = {task.id for task in filtered_task_list}

    # Act
    user_task_plan_list = await repo_task.plan_lst(
        user_id=user.id, filter_obj=filter_obj, sorting_obj=SortUserTaskObj(), iterable_obj=IterableObj()
    )

    user_task_set_user_id = {user_task.user_id for user_task in user_task_plan_list.items}
    user_task_set_task_id = {user_task.task_id for user_task in user_task_plan_list.items}

    # Assert
    assert len(user_task_plan_list.items) == total
    assert user_task_set_task_id == asrt_task_set_id
    assert user_task_set_user_id == set([user.id])

    if filter_obj.task_active is not None:
        asrt_task_dict_active = {
            task.id: task.active for task in filtered_task_list if task.active == filter_obj.task_active
        }

        for task_id in user_task_set_task_id:
            assert task_id in asrt_task_dict_active
            assert asrt_task_dict_active[task_id] == filter_obj.task_active

    if filter_obj.category_id is not None:
        asrt_task_dict_category_id = {task.id: task.category_id for task in filtered_task_list}

        for task_id in user_task_set_task_id:
            assert task_id in asrt_task_dict_category_id
            assert asrt_task_dict_category_id[task_id] == filter_obj.category_id
