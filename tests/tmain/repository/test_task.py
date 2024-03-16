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
from src.core.interfaces.repository.challenges.task import IRepositoryTask, TaskFilter
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
    repo_task: IRepositoryTask,  # user_task_id: int, user_task_status: OccupancyStatusEnum
):
    # Arrange
    user = await dl.user_loader.create()
    asrt_user_task = await dl.create_user_task(user=user, status=OccupancyStatusEnum.ACTIVE)

    # Act && Assert
    with pytest.raises(EntityNotChange) as e:
        await repo_task.user_task_update(user_id=user.id, id=asrt_user_task.id, obj=TaskUserUpdateDTO())

    assert "Empty data for update" in str(e.value)


# # pytest tests/tmain/repository/test_task.py::test_user_task_update_error -v -s
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "user_task_id, user_task_status",
#     [[100, OccupancyStatusEnum.OVERDUE], [1984, OccupancyStatusEnum.FINISH], [100, OccupancyStatusEnum.REJECT]],
# )
# async def test_user_task_update_error(
#     dl: dataloader, repo_task: IRepositoryTask, user_task_id: int, user_task_status: OccupancyStatusEnum
# ):
#     # Arrange
#     task_id_set = await _test_get_set_of_tasks(dl=dl)
#     user_id, *_ = await _test_user_task_list(dl=dl, task_id_set=task_id_set)
#     update_obj = TaskUserUpdateDTO(status=user_task_status)

#     # Assert
#     with pytest.raises(EntityNotFound) as e:
#         await repo_task.user_task_update(user_id=user_id, id=user_task_id, obj=update_obj)
#     assert f"UserTask object={user_task_id} not found and was not updated" in str(e.value)


# # pytest tests/tmain/repository/test_task.py::test_user_plan_create_error -v -s
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "create_obj",
#     [
#         TaskUserPlanCreateDTO(user_id="destroy", task_id=1),
#         TaskUserPlanCreateDTO(user_id="boys", task_id=3),
#     ],
# )
# async def test_user_plan_create_error(dl: dataloader, repo_task: IRepositoryTask, create_obj: TaskUserPlanCreateDTO):
#     # Arrange
#     await dl.user_loader.create(id=create_obj.user_id)

#     # Act
#     with pytest.raises(EntityNotCreated) as e:
#         await repo_task.plan_create(obj=create_obj)

#     # Assert
#     assert "Not found fk" in str(e.value)


# async def _test_user_task_get_plan_list(
#     dl: dataloader, task_id_set: set[int], user_id: str | None = None, task_id: int | None = None
# ):
#     user = await dl.user_loader.create(id=user_id)

#     if task_id in task_id_set:
#         task_id_set.remove(task_id)

#     for task_id in task_id_set:
#         await dl.user_task_plan.create(user_id=user.id, task_id=task_id)

#     return user_id


# # pytest tests/tmain/repository/test_task.py::test_user_plan_create_ok -v -s
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "create_obj, assrt_obj",
#     [
#         [TaskUserPlanCreateDTO(user_id="destroy", task_id=1), TaskUserPlan(user_id="destroy", task_id=1)],
#         [TaskUserPlanCreateDTO(user_id="boys", task_id=3), TaskUserPlan(user_id="boys", task_id=3)],
#     ],
# )
# async def test_user_plan_create_ok(
#     dl: dataloader, repo_task: IRepositoryTask, create_obj: TaskUserPlanCreateDTO, assrt_obj: TaskUserPlan
# ):
#     # Arrange
#     task_id_set = await _test_get_set_of_tasks(dl=dl, task_id=create_obj.task_id)
#     await _test_user_task_get_plan_list(
#         dl=dl, task_id_set=task_id_set, user_id=create_obj.user_id, task_id=create_obj.task_id
#     )

#     # Act
#     user_task_plan_create = await repo_task.plan_create(obj=create_obj)

#     # Assert
#     assert user_task_plan_create.task_id == assrt_obj.task_id
#     assert user_task_plan_create.user_id == assrt_obj.user_id


# # pytest tests/tmain/repository/test_task.py::test_user_plan_delete_ok -v -s
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "delete_obj, assrt_obj",
#     [
#         [TaskUserPlanCreateDTO(user_id="destroy", task_id=1), TaskUserPlan(user_id="destroy", task_id=1)],
#         [TaskUserPlanCreateDTO(user_id="boys", task_id=3), TaskUserPlan(user_id="boys", task_id=3)],
#     ],
# )
# async def test_user_plan_delete_ok(
#     dl: dataloader, repo_task: IRepositoryTask, delete_obj: TaskUserPlanCreateDTO, assrt_obj: TaskUserPlan
# ):
#     # Arrange
#     task_id_set = await _test_get_set_of_tasks(dl=dl, task_id=delete_obj.task_id)
#     await _test_user_task_get_plan_list(dl=dl, task_id_set=task_id_set, user_id=delete_obj.user_id)

#     # Act
#     user_task_plan_delete = await repo_task.plan_delete(user_id=delete_obj.user_id, task_id=delete_obj.task_id)

#     # Assert
#     assert user_task_plan_delete.task_id == assrt_obj.task_id
#     assert user_task_plan_delete.user_id == assrt_obj.user_id


# # pytest tests/tmain/repository/test_task.py::test_user_task_plan_delete_task_not_found_error -v -s
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "delete_obj",
#     [
#         dict(user_id="destroy", task_id=1),
#         dict(user_id="boys", task_id=3),
#     ],
# )
# async def test_user_task_plan_delete_task_not_found_error(dl: dataloader, repo_task: IRepositoryTask, delete_obj: dict):
#     # Arrange
#     user_id, task_id = delete_obj.values()
#     user = await dl.user_loader.create(id=user_id)

#     # Act
#     with pytest.raises(EntityNotFound) as e:
#         await repo_task.plan_delete(user_id=user_id, task_id=task_id)

#     # Assert
#     assert f"UserTaskPlan with task_id={task_id}, user_id={user_id} not deleted" in str(e.value)
