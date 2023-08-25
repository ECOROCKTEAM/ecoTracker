import pytest

from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive, PrivacyError
from src.core.exception.user import PermissionError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_public_add_user import GroupPublicAddUserUsecase
from tests.fixtures.const import DEFAULT_TEST_USECASE_GROUP_ID
from tests.fixtures.group.usecase.group import (
    mock_group_get_active_private,
    mock_group_get_default,
    mock_group_get_not_active,
)
from tests.fixtures.group.usecase.user import mock_group_user_add_user
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/group/usecases/user/test_public_user_add.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_user_add_user: UserGroupDTO,
):
    uc = GroupPublicAddUserUsecase(uow=uow)
    res = await uc(user=fxe_user_default, group_id=mock_group_get_default.id)
    group_user = res.item
    assert isinstance(group_user, UserGroupDTO)
    assert group_user.role == GroupRoleEnum.USER


# pytest tests/main/group/usecases/user/test_public_user_add.py::test_group_not_active_fail -v -s
@pytest.mark.asyncio
async def test_group_not_active_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_not_active: Group,
):
    uc = GroupPublicAddUserUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(user=fxe_user_default, group_id=mock_group_get_not_active.id)


# pytest tests/main/group/usecases/user/test_public_user_add.py::test_group_not_public_fail -v -s
@pytest.mark.asyncio
async def test_group_not_public_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_active_private: Group,
):
    uc = GroupPublicAddUserUsecase(uow=uow)
    with pytest.raises(PrivacyError):
        await uc(user=fxe_user_default, group_id=mock_group_get_active_private.id)
