import pytest

from src.core.dto.group.group import GroupCreateDTO
from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.exception.base import LogicError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_leave import GroupLeaveUsecase
from tests.fixtures.const import DEFAULT_TEST_USECASE_GROUP_ID
from tests.fixtures.group.usecase.user import (
    mock_group_user_get_admin,
    mock_group_user_get_superuser,
    mock_group_user_get_user,
    mock_group_user_list_ret_superusers_1,
    mock_group_user_list_ret_superusers_10,
    mock_group_user_remove,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/group/usecases/group/test_leave.py::test_ok_user -v -s
@pytest.mark.asyncio
async def test_ok_user(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_user_get_user: UserGroupDTO,
    mock_group_user_remove: bool,
):
    uc = GroupLeaveUsecase(uow=uow)
    res = await uc(user=fxe_user_default, group_id=DEFAULT_TEST_USECASE_GROUP_ID)
    check = res.item
    assert check is True


# pytest tests/main/group/usecases/group/test_leave.py::test_ok_admin -v -s
@pytest.mark.asyncio
async def test_ok_admin(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_user_get_admin: UserGroupDTO,
    mock_group_user_remove: bool,
):
    uc = GroupLeaveUsecase(uow=uow)
    res = await uc(user=fxe_user_default, group_id=DEFAULT_TEST_USECASE_GROUP_ID)
    check = res.item
    assert check is True


# pytest tests/main/group/usecases/group/test_leave.py::test_ok_superuser -v -s
@pytest.mark.asyncio
async def test_ok_superuser(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_user_get_superuser: UserGroupDTO,
    mock_group_user_list_ret_superusers_10: list[UserGroupDTO],
    mock_group_user_remove: bool,
):
    uc = GroupLeaveUsecase(uow=uow)
    res = await uc(user=fxe_user_default, group_id=DEFAULT_TEST_USECASE_GROUP_ID)
    check = res.item
    assert check is True


# pytest tests/main/group/usecases/group/test_leave.py::test_superuser_fail -v -s
@pytest.mark.asyncio
async def test_superuser_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_user_get_superuser: UserGroupDTO,
    mock_group_user_list_ret_superusers_1: list[UserGroupDTO],
):
    uc = GroupLeaveUsecase(uow=uow)
    with pytest.raises(LogicError):
        await uc(user=fxe_user_default, group_id=DEFAULT_TEST_USECASE_GROUP_ID)
