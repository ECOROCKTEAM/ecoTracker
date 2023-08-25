import pytest

from src.core.dto.group.group import GroupCreateDTO
from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.exception.user import PermissionError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_delete import GroupDeleteUsecase
from tests.fixtures.const import DEFAULT_TEST_USECASE_GROUP_ID
from tests.fixtures.group.usecase.group import mock_group_deactivate
from tests.fixtures.group.usecase.user import (
    mock_group_user_get_superuser,
    mock_group_user_get_user,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/group/usecases/group/test_delete.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_deactivate: int,
    mock_group_user_get_superuser: UserGroupDTO,
):
    uc = GroupDeleteUsecase(uow=uow)
    res = await uc(user=fxe_user_default, group_id=DEFAULT_TEST_USECASE_GROUP_ID)
    group_id = res.item
    assert group_id == DEFAULT_TEST_USECASE_GROUP_ID


# pytest tests/main/group/usecases/group/test_delete.py::test_user_not_superuser -v -s
@pytest.mark.asyncio
async def test_user_not_superuser(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_deactivate: int,
    mock_group_user_get_user: UserGroupDTO,
):
    uc = GroupDeleteUsecase(uow=uow)
    with pytest.raises(PermissionError):
        await uc(user=fxe_user_default, group_id=DEFAULT_TEST_USECASE_GROUP_ID)
