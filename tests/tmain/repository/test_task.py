from datetime import datetime
from random import choice

import pytest

from src.core.const.translate import DEFAULT_LANGUANGE
from src.core.dto.challenges.task import (
    TaskUserCreateDTO,
    TaskUserPlanCreateDTO,
    TaskUserUpdateDTO,
)
from src.core.entity.task import TaskUserPlan
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.task import IRepositoryTask
from tests.dataloader import dataloader


async def _test_get_set_of_tasks(
    dl: dataloader,
    task_id: int | None = None,
) -> set[int]:
    task_id_counter = 0
    task_id_set = set()

    if task_id is not None:
        task_id_counter += task_id

    for _ in range(10):
        category = await dl.category_loader.create()
        for e in LanguageEnum:
            await dl.category_translate_loader.create(category=category, language=e)

        for _ in range(3):
            task = await dl.task_loader.create(category=category, id=task_id_counter)
            for e in LanguageEnum:
                await dl.task_translate_loader.create(task_id=task.id, language=e)

            task_id_set.add(task.id)
            task_id_counter += 1

    return task_id_set


# pytest tests/tmain/repository/test_task.py::test_get_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("task_id, lang", [[1, DEFAULT_LANGUANGE], [50, LanguageEnum.FR], [100, LanguageEnum.RU]])
async def test_get_ok(dl: dataloader, repo_task: IRepositoryTask, task_id: int, lang: LanguageEnum):
    # Arrange
    await _test_get_set_of_tasks(dl=dl, task_id=task_id)

    # Act
    task = await repo_task.get(id=task_id, lang=lang)

    # Assert
    assert task_id == task.id
    assert lang == task.language


# pytest tests/tmain/repository/test_task.py::test_get_language_not_found_error -v -s
@pytest.mark.asyncio
async def test_get_language_not_found_error(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    category = await dl.category_loader.create()
    for e in LanguageEnum:
        await dl.category_translate_loader.create(category=category, language=e)

    # Act
    task = await dl.task_loader.create(category=category)
    with pytest.raises(TranslateNotFound) as e:
        await repo_task.get(id=task.id, lang=DEFAULT_LANGUANGE)

    # Assert
    assert f"with task_translate=None" in str(e.value)


# pytest tests/tmain/repository/test_task.py::test_get_task_not_found_error -v -s
@pytest.mark.asyncio
async def test_get_task_not_found_error(dl: dataloader, repo_task: IRepositoryTask):
    # Arrange
    task_id_list = await _test_get_set_of_tasks(dl=dl)

    # Act
    non_exist_id = sum(task_id_list)
    with pytest.raises(EntityNotFound) as e:
        await repo_task.get(id=non_exist_id, lang=DEFAULT_LANGUANGE)

    # Assert
    assert f"Task.id={non_exist_id} not found" in str(e.value)


# pytest tests/tmain/repository/test_task.py::test_user_task_add_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("task_id", [1, 50, 100])
async def test_user_task_add_ok(dl: dataloader, repo_task: IRepositoryTask, task_id: int):
    # Arrange
    await _test_get_set_of_tasks(dl=dl, task_id=task_id)
    user = await dl.user_loader.create()

    # Act
    user_task_add = await repo_task.user_task_add(user_id=user.id, obj=TaskUserCreateDTO(task_id=task_id))

    # Assert
    assert user_task_add.task_id == task_id
    assert user_task_add.user_id == user.id
    assert user_task_add.status == OccupancyStatusEnum.ACTIVE
    assert isinstance(user_task_add.date_start, datetime)
    assert user_task_add.date_close is None


# pytest tests/tmain/repository/test_task.py::test_user_task_add_not_created_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("task_id", [100, 1000, 1984])
async def test_user_task_add_not_created_error(dl: dataloader, repo_task: IRepositoryTask, task_id: int):
    # Arrange
    await _test_get_set_of_tasks(dl=dl)
    user = await dl.user_loader.create()

    # Act
    create_obj = TaskUserCreateDTO(task_id=task_id)

    # Assert
    with pytest.raises(EntityNotCreated) as e:
        await repo_task.user_task_add(user_id=user.id, obj=create_obj)
    assert "Not found fk" in str(e.value)


async def _test_user_task_list(
    dl: dataloader,
    task_id_set: set[int],
    user_id: str | None = None,
    user_task_id: int | None = None,
    user_task_status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE,
) -> tuple[str, set[int], int | None]:
    fake_user = await dl.user_loader.create()
    user = await dl.user_loader.create(id=user_id)

    task_id_list = list(task_id_set)
    id_counter = 0
    target_task_id = None

    if user_task_id is not None:
        task_id = choice(task_id_list)
        target_task_id = task_id
        if user_task_status == OccupancyStatusEnum.ACTIVE:
            task_id_list.remove(task_id)

        await dl.user_task_loader.create(id=user_task_id, user_id=user.id, task_id=task_id, status=user_task_status)
        id_counter += user_task_id

    while len(task_id_list) != len(task_id_set) // 2:
        enum = choice(list(OccupancyStatusEnum))
        task_id = choice(task_id_list)
        if enum == OccupancyStatusEnum.ACTIVE:
            task_id_list.remove(task_id)

        id_counter += 1
        await dl.user_task_loader.create(id=id_counter, user_id=user.id, task_id=task_id, status=enum)

    added_task_id_set = task_id_set - set(task_id_list)
    return user.id, added_task_id_set, target_task_id


# pytest tests/tmain/repository/test_task.py::test_user_task_get_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("user_task_id", [1, 100, 1984])
async def test_user_task_get_ok(dl: dataloader, repo_task: IRepositoryTask, user_task_id: int):
    # Arrange
    task_id_set = await _test_get_set_of_tasks(dl=dl)
    user_id, *_, target_task_id = await _test_user_task_list(dl=dl, task_id_set=task_id_set, user_task_id=user_task_id)

    # Act
    user_task = await repo_task.user_task_get(user_id=user_id, id=user_task_id)

    # Assert

    assert user_task.id == user_task_id
    assert user_task.task_id == target_task_id
    assert user_task.user_id == user_id
    assert isinstance(user_task.status, OccupancyStatusEnum)


# pytest tests/tmain/repository/test_task.py::test_user_task_get_not_found_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("user_task_id", [1000, 100, 1984])
async def test_user_task_get_not_found_error(dl: dataloader, repo_task: IRepositoryTask, user_task_id: int):
    # Arrange
    task_id_set = await _test_get_set_of_tasks(dl=dl)
    user_id, *_ = await _test_user_task_list(dl=dl, task_id_set=task_id_set)

    # Act
    with pytest.raises(EntityNotFound) as e:
        await repo_task.user_task_get(user_id=user_id, id=user_task_id)

    # Assert
    assert f"UserTask object with id={user_task_id} not found" in str(e.value)


# pytest tests/tmain/repository/test_task.py::test_user_task_update_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_task_id, user_task_status",
    [[1, OccupancyStatusEnum.OVERDUE], [10, OccupancyStatusEnum.FINISH], [100, OccupancyStatusEnum.REJECT]],
)
async def test_user_task_update_ok(
    dl: dataloader, repo_task: IRepositoryTask, user_task_id: int, user_task_status: OccupancyStatusEnum
):
    # Arrange
    task_id_set = await _test_get_set_of_tasks(dl=dl)
    user_id, *_, target_task_id = await _test_user_task_list(dl=dl, task_id_set=task_id_set, user_task_id=user_task_id)
    update_obj = TaskUserUpdateDTO(status=user_task_status)

    # Act
    user_task_complete = await repo_task.user_task_update(user_id=user_id, id=user_task_id, obj=update_obj)

    # Assert
    assert user_task_id == user_task_complete.id
    assert user_id == user_task_complete.user_id
    assert target_task_id == user_task_complete.task_id
    assert user_task_complete.status == update_obj.status

    if user_task_complete.status in [OccupancyStatusEnum.FINISH, OccupancyStatusEnum.REJECT]:
        assert user_task_complete.date_close.timestamp() == update_obj.date_close.timestamp()  # type: ignore None type skip


# pytest tests/tmain/repository/test_task.py::test_user_task_update_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_task_id, user_task_status",
    [[100, OccupancyStatusEnum.OVERDUE], [1984, OccupancyStatusEnum.FINISH], [100, OccupancyStatusEnum.REJECT]],
)
async def test_user_task_update_error(
    dl: dataloader, repo_task: IRepositoryTask, user_task_id: int, user_task_status: OccupancyStatusEnum
):
    # Arrange
    task_id_set = await _test_get_set_of_tasks(dl=dl)
    user_id, *_ = await _test_user_task_list(dl=dl, task_id_set=task_id_set)
    update_obj = TaskUserUpdateDTO(status=user_task_status)

    # Assert
    with pytest.raises(EntityNotFound) as e:
        await repo_task.user_task_update(user_id=user_id, id=user_task_id, obj=update_obj)
    assert f"UserTask object={user_task_id} not found and was not updated" in str(e.value)


# pytest tests/tmain/repository/test_task.py::test_user_plan_create_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_obj",
    [
        TaskUserPlanCreateDTO(user_id="destroy", task_id=1),
        TaskUserPlanCreateDTO(user_id="boys", task_id=3),
    ],
)
async def test_user_plan_create_error(dl: dataloader, repo_task: IRepositoryTask, create_obj: TaskUserPlanCreateDTO):
    # Arrange
    await dl.user_loader.create(id=create_obj.user_id)

    # Act
    with pytest.raises(EntityNotCreated) as e:
        await repo_task.plan_create(obj=create_obj)

    # Assert
    assert "Not found fk" in str(e.value)


async def _test_user_task_get_plan_list(
    dl: dataloader, task_id_set: set[int], user_id: str | None = None, task_id: int | None = None
):
    user = await dl.user_loader.create(id=user_id)

    if task_id in task_id_set:
        task_id_set.remove(task_id)

    for task_id in task_id_set:
        await dl.user_task_plan.create(user_id=user.id, task_id=task_id)

    return user_id


# pytest tests/tmain/repository/test_task.py::test_user_plan_create_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_obj, assrt_obj",
    [
        [TaskUserPlanCreateDTO(user_id="destroy", task_id=1), TaskUserPlan(user_id="destroy", task_id=1)],
        [TaskUserPlanCreateDTO(user_id="boys", task_id=3), TaskUserPlan(user_id="boys", task_id=3)],
    ],
)
async def test_user_plan_create_ok(
    dl: dataloader, repo_task: IRepositoryTask, create_obj: TaskUserPlanCreateDTO, assrt_obj: TaskUserPlan
):
    # Arrange
    task_id_set = await _test_get_set_of_tasks(dl=dl, task_id=create_obj.task_id)
    await _test_user_task_get_plan_list(
        dl=dl, task_id_set=task_id_set, user_id=create_obj.user_id, task_id=create_obj.task_id
    )

    # Act
    user_task_plan_create = await repo_task.plan_create(obj=create_obj)

    # Assert
    assert user_task_plan_create.task_id == assrt_obj.task_id
    assert user_task_plan_create.user_id == assrt_obj.user_id


# pytest tests/tmain/repository/test_task.py::test_user_plan_delete_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "delete_obj, assrt_obj",
    [
        [TaskUserPlanCreateDTO(user_id="destroy", task_id=1), TaskUserPlan(user_id="destroy", task_id=1)],
        [TaskUserPlanCreateDTO(user_id="boys", task_id=3), TaskUserPlan(user_id="boys", task_id=3)],
    ],
)
async def test_user_plan_delete_ok(
    dl: dataloader, repo_task: IRepositoryTask, delete_obj: TaskUserPlanCreateDTO, assrt_obj: TaskUserPlan
):
    # Arrange
    task_id_set = await _test_get_set_of_tasks(dl=dl, task_id=delete_obj.task_id)
    await _test_user_task_get_plan_list(dl=dl, task_id_set=task_id_set, user_id=delete_obj.user_id)

    # Act
    user_task_plan_delete = await repo_task.plan_delete(user_id=delete_obj.user_id, task_id=delete_obj.task_id)

    # Assert
    assert user_task_plan_delete.task_id == assrt_obj.task_id
    assert user_task_plan_delete.user_id == assrt_obj.user_id


# pytest tests/tmain/repository/test_task.py::test_user_task_plan_delete_task_not_found_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "delete_obj",
    [
        dict(user_id="destroy", task_id=1),
        dict(user_id="boys", task_id=3),
    ],
)
async def test_user_task_plan_delete_task_not_found_error(dl: dataloader, repo_task: IRepositoryTask, delete_obj: dict):
    # Arrange
    user_id, task_id = delete_obj.values()
    user = await dl.user_loader.create(id=user_id)

    # Act
    with pytest.raises(EntityNotFound) as e:
        await repo_task.plan_delete(user_id=user_id, task_id=task_id)

    # Assert
    assert f"UserTaskPlan with task_id={task_id}, user_id={user_id} not deleted" in str(e.value)
