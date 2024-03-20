from datetime import datetime

import pytest

from src.core.const.task import MAX_TASK_AMOUNT_NOT_PREMIUM, MAX_TASK_AMOUNT_PREMIUM
from src.core.dto.utils import IterableObj, SortObj
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import (
    EntityAlreadyUsage,
    EntityNotActive,
    EntityNotChange,
    MaxAmountError,
)
from src.core.interfaces.repository.challenges.task import (
    SortUserTaskObj,
    TaskFilter,
    TaskUserFilter,
    TaskUserPlanFilter,
)
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.task.task_get import TaskGetUsecase
from src.core.usecases.challenges.task.task_list import TaskListUsecase
from src.core.usecases.challenges.task.task_user_add import UserTaskAddUsecase
from src.core.usecases.challenges.task.task_user_complete import UserTaskCompleteUsecase
from src.core.usecases.challenges.task.task_user_get import UserTaskGetUsecase
from src.core.usecases.challenges.task.task_user_list import UserTaskListUsecase
from src.core.usecases.challenges.task.task_user_plan_list import (
    UserTaskPlanListUsecase,
)
from src.core.usecases.challenges.task.task_user_reject import UserTaskRejectUsecase
from src.data.models.challenges.task import UserTaskModel
from src.data.models.user.user import UserScoreModel
from src.data.repository.user import model_to_dto as user_model_to_dto
from tests.dataloader import dataloader


# pytest tests/tmain/usecase/test_task.py::test_task_get_ok -v -s
@pytest.mark.asyncio
async def test_task_get_ok(
    dl: dataloader,
    uow: IUnitOfWork,
):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)
    await dl.user_loader.create()

    task = await dl.create_task()
    await dl.create_task()

    # Act
    uc = TaskGetUsecase(uow=uow)
    res = await uc(user=user, id=task.id)

    # Assert
    assert res.item.id == task.id
    assert res.item.active == task.active
    assert res.item.category_id == task.category_id
    assert res.item.score == task.score
    assert res.item.language == user.language


# pytest tests/tmain/usecase/test_task.py::test_task_get_task_not_active_error -v -s
@pytest.mark.asyncio
async def test_task_get_task_not_active_error(dl: dataloader, uow: IUnitOfWork):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    task = await dl.create_task(active=False)
    await dl.create_task(active=True)

    # Act
    uc = TaskGetUsecase(uow=uow)
    with pytest.raises(EntityNotActive) as e:
        await uc(user=user, id=task.id)

    # Assert
    assert f"task.id={task.id}" in str(e.value)


# pytest tests/tmain/usecase/test_task.py::test_task_list_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("count", [0, 10])
async def test_task_list_ok(dl: dataloader, uow: IUnitOfWork, count: int):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    task_list = await dl.create_task_list_random(count=count)
    active_task_id_set = {task.id for task in task_list if task.active}

    # Act
    uc = TaskListUsecase(uow=uow)
    res = await uc(
        user=user,
        filter_obj=TaskFilter(),
        sorting_obj=SortObj(),
        iterable_obj=IterableObj(),
    )
    res_task_id_set = {task.id for task in res.items}

    # Assert
    assert active_task_id_set == res_task_id_set


# pytest tests/tmain/usecase/test_task.py::test_user_task_add_task_not_active_error -v -s
@pytest.mark.asyncio
async def test_user_task_add_task_not_active_error(dl: dataloader, uow: IUnitOfWork):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    await dl.create_task_list_random()
    task = await dl.create_task(active=False)

    # Act
    uc = UserTaskAddUsecase(uow=uow)
    with pytest.raises(EntityNotActive) as e:
        await uc(user=user, task_id=task.id)

    # Assert
    assert f"task.id={task.id}" in str(e.value)


# pytest tests/tmain/usecase/test_task.py::test_user_task_add_task_already_usage_error -v -s
@pytest.mark.asyncio
async def test_user_task_add_task_already_usage_error(dl: dataloader, uow: IUnitOfWork):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)
    task_already_usage = await dl.create_task()

    await dl.create_task_list_random()
    await dl.create_user_task(user=user_model, task=task_already_usage, status=OccupancyStatusEnum.ACTIVE)

    # Act
    uc = UserTaskAddUsecase(uow=uow)
    with pytest.raises(EntityAlreadyUsage) as e:
        await uc(user=user, task_id=task_already_usage.id)

    # Assert
    assert f"{user.id=}, task.id={task_already_usage.id}" in str(e.value)


async def _arrange_user_not_premium(dl: dataloader) -> User:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)
    user.is_premium = False
    await dl.create_user_task_plan_list(user=user_model, count=MAX_TASK_AMOUNT_NOT_PREMIUM)
    return user


async def _arrange_user_premium(dl: dataloader) -> User:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)
    await dl.create_user_task_plan_list(user=user_model, count=MAX_TASK_AMOUNT_PREMIUM)
    return user


# pytest tests/tmain/usecase/test_task.py::test_user_task_add_max_amount_plan_list_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_user", [_arrange_user_not_premium, _arrange_user_premium])
async def test_user_task_add_max_amount_plan_list_error(dl: dataloader, uow: IUnitOfWork, arrange_user):
    # Arrange
    user = await arrange_user(dl=dl)
    task = await dl.create_task()

    # Act
    uc = UserTaskAddUsecase(uow=uow)
    with pytest.raises(MaxAmountError) as e:
        await uc(user=user, task_id=task.id)

    # Assert
    assert f"User={user.id=} has max plan tasks" in str(e.value)


async def _arrange_premium_user_task_active_list(dl: dataloader) -> User:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    await dl.create_user_task_list(
        user=user_model, count=MAX_TASK_AMOUNT_PREMIUM, status_list=[OccupancyStatusEnum.ACTIVE]
    )
    return user


async def _arrange_not_premium_user_task_active_list(dl: dataloader) -> User:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)
    user.is_premium = False

    await dl.create_user_task_list(
        user=user_model, count=MAX_TASK_AMOUNT_NOT_PREMIUM, status_list=[OccupancyStatusEnum.ACTIVE]
    )
    return user


# pytest tests/tmain/usecase/test_task.py::test_user_task_max_amount_active_tasks_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_user", [_arrange_not_premium_user_task_active_list, _arrange_premium_user_task_active_list]
)
async def test_user_task_max_amount_active_tasks_error(dl: dataloader, uow: IUnitOfWork, arrange_user):
    # Arrange
    task = await dl.create_task()
    user = await arrange_user(dl=dl)

    # Act
    uc = UserTaskAddUsecase(uow=uow)
    with pytest.raises(MaxAmountError) as e:
        await uc(user=user, task_id=task.id)

    # Assert
    assert f"User={user.id=} has max active tasks" in str(e.value)


# pytest tests/tmain/usecase/test_task.py::test_user_task_add_ok -v -s
@pytest.mark.asyncio
async def test_user_task_add_ok(dl: dataloader, uow: IUnitOfWork):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)
    task = await dl.create_task()

    await dl.create_task()

    # Act
    uc = UserTaskAddUsecase(uow=uow)
    res = await uc(user=user, task_id=task.id)

    # Assert
    assert res.item.status == OccupancyStatusEnum.ACTIVE
    assert user.id == res.item.user_id
    assert task.id == res.item.task_id
    assert isinstance(res.item.date_start, datetime)

    await dl._delete(model=UserTaskModel, attr="id", pk=res.item.id)


# pytest tests/tmain/usecase/test_task.py::test_user_task_complete_ok -v -s
@pytest.mark.asyncio
async def test_user_task_complete_ok(dl: dataloader, uow: IUnitOfWork):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    user_task = await dl.create_user_task(user=user_model, status=OccupancyStatusEnum.ACTIVE)
    await dl.create_user_task_list(user=user_model)

    # Act
    uc = UserTaskCompleteUsecase(uow=uow)
    res = await uc(user=user, id=user_task.id)

    # Assert
    assert res.item.id == user_task.id
    assert res.item.status == OccupancyStatusEnum.FINISH
    assert res.item.task_id == user_task.task_id
    assert res.item.user_id == user.id
    assert isinstance(res.item.date_close, datetime)
    assert isinstance(res.item.date_start, datetime)

    # Нужно ли проверять работу метода зачисления очков юзеру в нашем uc? (uow.score_user.add)

    await dl._delete(model=UserTaskModel, attr="id", pk=user_task.id)
    await dl._delete(model=UserScoreModel, attr="user_id", pk=user_model.id)


# pytest tests/tmain/usecase/test_task.py::test_user_task_complete_task_status_not_active -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_task_status", [OccupancyStatusEnum.OVERDUE, OccupancyStatusEnum.REJECT, OccupancyStatusEnum.FINISH]
)
async def test_user_task_complete_task_status_not_active(
    dl: dataloader, uow: IUnitOfWork, user_task_status: OccupancyStatusEnum
):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    user_task = await dl.create_user_task(user=user_model, status=user_task_status)

    # Act
    uc = UserTaskCompleteUsecase(uow=uow)
    with pytest.raises(EntityNotChange) as e:
        await uc(user=user, id=user_task.id)

    # Assert
    assert f"user_task.id={user_task.id}"


# # pytest tests/tmain/usecase/test_task.py::test_user_task_complete_user_not_premium -v -s
# @pytest.mark.asyncio
# async def test_user_task_complete_user_not_premium(dl: dataloader, uow: IUnitOfWork):
#     ...


# # pytest tests/tmain/usecase/test_task.py::test_user_task_complete_user_premium -v -s
# @pytest.mark.asyncio
# async def test_user_task_complete_user_premium(dl: dataloader, uow: IUnitOfWork):
#     ...


# pytest tests/tmain/usecase/test_task.py::test_user_task_get_ok -v -s
@pytest.mark.asyncio
async def test_user_task_get_ok(dl: dataloader, uow: IUnitOfWork):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    user_task = await dl.create_user_task(user=user_model)
    await dl.create_user_task(user=user_model)

    # Act
    uc = UserTaskGetUsecase(uow=uow)
    res = await uc(user=user, id=user_task.id)

    # Assert
    assert res.item.id == user_task.id
    assert res.item.task_id == user_task.task_id
    assert res.item.user_id == user_task.user_id == user.id
    assert isinstance(res.item.date_start, datetime)


# pytest tests/tmain/usecase/test_task.py::test_user_task_list_ok -v -s
@pytest.mark.asyncio
async def test_user_task_list_ok(dl: dataloader, uow: IUnitOfWork):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    user_task_list = await dl.create_user_task_list(user=user_model)
    arrange_user_task_id_set = {user_task.id for user_task in user_task_list}

    # Act
    uc = UserTaskListUsecase(uow=uow)
    res = await uc(user=user, filter_obj=TaskUserFilter(), sorting_obj=SortUserTaskObj(), iterable_obj=IterableObj())

    res_user_task_id_set = {user_task.id for user_task in res.items}
    res_user_id_set = {user_task.user_id for user_task in res.items}

    # Assert
    assert res_user_task_id_set == arrange_user_task_id_set
    assert res_user_id_set == set([user.id])


# pytest tests/tmain/usecase/test_task.py::test_user_plan_list_ok -v -s
@pytest.mark.asyncio
async def test_user_plan_list_ok(dl: dataloader, uow: IUnitOfWork):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    user_task_plan_list = await dl.create_user_task_plan_list(user=user_model)
    user_task_plan_task_id_set = {user_task.task_id for user_task in user_task_plan_list}

    # Act
    uc = UserTaskPlanListUsecase(uow=uow)
    res = await uc(
        user=user, filter_obj=TaskUserPlanFilter(), sorting_obj=SortUserTaskObj(), iterable_obj=IterableObj()
    )
    res_task_id_set = {user_task.task_id for user_task in res.items}
    res_user_id_set = {user_task.user_id for user_task in res.items}

    # Assert
    assert res_task_id_set == user_task_plan_task_id_set
    assert res_user_id_set == set([user.id])


# pytest tests/tmain/usecase/test_task.py::test_user_task_reject_ok -v -s
@pytest.mark.asyncio
async def test_user_task_reject_ok(dl: dataloader, uow: IUnitOfWork):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    user_task = await dl.create_user_task(user=user_model)
    await dl.create_user_task(user=user_model)
    await dl.create_user_task(user=user_model, status=OccupancyStatusEnum.REJECT)

    # Act
    uc = UserTaskRejectUsecase(uow=uow)
    res = await uc(user=user, id=user_task.id)

    # Assert
    assert res.item.id == user_task.id
    assert res.item.task_id == user_task.task_id
    assert res.item.user_id == user_task.user_id
    assert res.item.status == OccupancyStatusEnum.REJECT
    assert isinstance(res.item.date_close, datetime)
    assert isinstance(res.item.date_start, datetime)


# pytest tests/tmain/usecase/test_task.py::test_user_task_reject_task_status_not_active_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_status", [OccupancyStatusEnum.REJECT, OccupancyStatusEnum.FINISH, OccupancyStatusEnum.OVERDUE]
)
async def test_user_task_reject_task_status_not_active_error(
    dl: dataloader, uow: IUnitOfWork, arrange_status: OccupancyStatusEnum
):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    user_task = await dl.create_user_task(user=user_model, status=arrange_status)

    # Act
    uc = UserTaskRejectUsecase(uow=uow)
    with pytest.raises(EntityNotChange) as e:
        await uc(user=user, id=user_task.id)

    # Assert
    assert f"user_task.id={user_task.id}" in str(e.value)


# # pytest tests/tmain/usecase/test_task.py::test_user_task_complete_user_premium -v -s
# @pytest.mark.asyncio
# async def test_user_task_reject_user_premium(dl: dataloader, uow: IUnitOfWork):
#     ...


# # pytest tests/tmain/usecase/test_task.py::test_user_task_complete_user_premium -v -s
# @pytest.mark.asyncio
# async def test_user_task_reject_user_premium(dl: dataloader, uow: IUnitOfWork):
#     ...
