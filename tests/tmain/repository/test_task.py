import random
from datetime import datetime
from random import choice

import pytest

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
from src.core.exception.base import EntityNotCreated, EntityNotFound, TranslateNotFound
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
    task_list = await repo_task.lst(
        filter_obj=fltr, sorting_obj=SortObj(), iterable_obj=IterableObj(), lang=LanguageEnum.EN
    )
    assert asrt_count == len(task_list.items)
    assert asrt_count == task_list.total


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
@pytest.mark.parametrize("flags", [(True, False), (False, True)])
async def test_user_task_add_not_created_error(dl: dataloader, repo_task: IRepositoryTask, flags: tuple[bool, bool]):
    # Arrange
    user_id, task_id = "-1", -1  # Default not exist id's
    user_flag, task_flag = flags
    if user_flag:
        user = await dl.user_loader.create()
        user_id = user.id
    if task_flag:
        task = await dl.create_task()
        task_id = task.id

    # Act && Assert
    with pytest.raises(EntityNotCreated) as e:
        await repo_task.user_task_add(user_id=user_id, obj=TaskUserCreateDTO(task_id=task_id))
    assert "Not found fk" in str(e.value)


# async def _test_user_task_list(
#     dl: dataloader,
#     task_id_set: set[int],
#     user_id: str | None = None,
#     user_task_id: int | None = None,
#     user_task_status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE,
# ) -> tuple[str, set[int], int | None]:
#     fake_user = await dl.user_loader.create()
#     user = await dl.user_loader.create(id=user_id)

#     task_id_list = list(task_id_set)
#     id_counter = 0
#     target_task_id = None

#     if user_task_id is not None:
#         task_id = choice(task_id_list)
#         target_task_id = task_id
#         if user_task_status == OccupancyStatusEnum.ACTIVE:
#             task_id_list.remove(task_id)

#         await dl.user_task_loader.create(id=user_task_id, user_id=user.id, task_id=task_id, status=user_task_status)
#         id_counter += user_task_id

#     while len(task_id_list) != len(task_id_set) // 2:
#         enum = choice(list(OccupancyStatusEnum))
#         task_id = choice(task_id_list)
#         if enum == OccupancyStatusEnum.ACTIVE:
#             task_id_list.remove(task_id)

#         id_counter += 1
#         await dl.user_task_loader.create(id=id_counter, user_id=user.id, task_id=task_id, status=enum)

#     added_task_id_set = task_id_set - set(task_id_list)
#     return user.id, added_task_id_set, target_task_id


# # pytest tests/tmain/repository/test_task.py::test_user_task_get_ok -v -s
# @pytest.mark.asyncio
# @pytest.mark.parametrize("user_task_id", [1, 100, 1984])
# async def test_user_task_get_ok(dl: dataloader, repo_task: IRepositoryTask, user_task_id: int):
#     # Arrange
#     task_id_set = await _test_get_set_of_tasks(dl=dl)
#     user_id, *_, target_task_id = await _test_user_task_list(dl=dl, task_id_set=task_id_set, user_task_id=user_task_id)

#     # Act
#     user_task = await repo_task.user_task_get(user_id=user_id, id=user_task_id)

#     # Assert

#     assert user_task.id == user_task_id
#     assert user_task.task_id == target_task_id
#     assert user_task.user_id == user_id
#     assert isinstance(user_task.status, OccupancyStatusEnum)


# # pytest tests/tmain/repository/test_task.py::test_user_task_get_not_found_error -v -s
# @pytest.mark.asyncio
# @pytest.mark.parametrize("user_task_id", [1000, 100, 1984])
# async def test_user_task_get_not_found_error(dl: dataloader, repo_task: IRepositoryTask, user_task_id: int):
#     # Arrange
#     task_id_set = await _test_get_set_of_tasks(dl=dl)
#     user_id, *_ = await _test_user_task_list(dl=dl, task_id_set=task_id_set)

#     # Act
#     with pytest.raises(EntityNotFound) as e:
#         await repo_task.user_task_get(user_id=user_id, id=user_task_id)

#     # Assert
#     assert f"UserTask object with id={user_task_id} not found" in str(e.value)


# # pytest tests/tmain/repository/test_task.py::test_user_task_update_ok -v -s
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "user_task_id, user_task_status",
#     [[1, OccupancyStatusEnum.OVERDUE], [10, OccupancyStatusEnum.FINISH], [100, OccupancyStatusEnum.REJECT]],
# )
# async def test_user_task_update_ok(
#     dl: dataloader, repo_task: IRepositoryTask, user_task_id: int, user_task_status: OccupancyStatusEnum
# ):
#     # Arrange
#     task_id_set = await _test_get_set_of_tasks(dl=dl)
#     user_id, *_, target_task_id = await _test_user_task_list(dl=dl, task_id_set=task_id_set, user_task_id=user_task_id)
#     update_obj = TaskUserUpdateDTO(status=user_task_status)

#     # Act
#     user_task_complete = await repo_task.user_task_update(user_id=user_id, id=user_task_id, obj=update_obj)

#     # Assert
#     assert user_task_id == user_task_complete.id
#     assert user_id == user_task_complete.user_id
#     assert target_task_id == user_task_complete.task_id
#     assert user_task_complete.status == update_obj.status

#     if user_task_complete.status in [OccupancyStatusEnum.FINISH, OccupancyStatusEnum.REJECT]:
#         assert user_task_complete.date_close.timestamp() == update_obj.date_close.timestamp()  # type: ignore None type skip


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
