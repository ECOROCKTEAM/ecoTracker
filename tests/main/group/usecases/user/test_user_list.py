import pytest

from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive, EntityNotFound
from src.core.exception.user import PermissionError
from src.core.interfaces.repository.group.group import GroupUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_user_list import GroupUserListUsecase
from src.data.repository.user import model_to_dto as user_model_to_dto
from tests.dataloader import dataloader


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_private_group_user_not_in_group_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_private_group_user_not_in_group_error(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PRIVATE)

    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter()
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group.id, filter_obj=filter_obj)
    assert "User outside a private group cannot see any users in it" in str(e.value)


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_user_in_publick_group_ok -v -s
@pytest.mark.asyncio
async def test_group_user_list_user_in_publick_group_ok(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.group_loader.create()

    await dl.user_group_loader.create(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER)

    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter()

    await uc(user=user, group_id=group.id, filter_obj=filter_obj)


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_user_not_in_group_with_blocked_filter_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_user_not_in_group_with_blocked_filter_error(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.group_loader.create()
    group_2 = await dl.group_loader.create()

    await dl.user_group_loader.create(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER)

    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter(role__in=[GroupRoleEnum.BLOCKED])
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group_2.id, filter_obj=filter_obj)
    assert "User cannot see BLOCKED users in public group" in str(e.value)


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_user_in_group_with_blocked_filter_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_user_in_group_with_blocked_filter_error(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.group_loader.create()

    await dl.user_group_loader.create(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER)

    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter(role__in=[GroupRoleEnum.BLOCKED])
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group.id, filter_obj=filter_obj)
    assert "User cannot see BLOCKED users in public group" in str(e.value)


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_group_not_active_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_group_not_active_error(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.group_loader.create(active=False)

    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter()
    with pytest.raises(EntityNotActive) as e:
        await uc(user=user, group_id=group.id, filter_obj=filter_obj)
    assert f"{group.id}" in str(e.value)


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_group_none_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_group_none_error(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group_id = 1

    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter()
    group_id = 123
    with pytest.raises(EntityNotFound) as e:
        await uc(user=user, group_id=group_id, filter_obj=filter_obj)
    assert f"{group_id}" in str(e.value)


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_user_blocked_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_user_blocked_error(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.group_loader.create()

    await dl.user_group_loader.create(user_id=user.id, group_id=group.id, role=GroupRoleEnum.BLOCKED)

    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter()
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group.id, filter_obj=filter_obj)
    assert f"is BLOCKED" in str(e.value)
