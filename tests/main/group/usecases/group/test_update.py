import pytest

from src.core.dto.group.group import GroupCreateDTO, GroupUpdateDTO
from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive, PermissionError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_update import GroupUpdateUsecase
from tests.fixtures.group.usecase.group import (
    mock_group_get_default,
    mock_group_get_not_active,
    mock_group_update,
)
from tests.fixtures.group.usecase.user import (
    mock_group_user_get_default,
    mock_group_user_get_user,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/group/usecases/group/test_update.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_update: Group,
    mock_group_user_get_default: UserGroupDTO,
):
    uc = GroupUpdateUsecase(uow=uow)
    res = await uc(user=fxe_user_default, group_id=mock_group_get_default.id, update_obj=GroupUpdateDTO())
    # active filter was changed to true
    group = res.item
    assert isinstance(group, Group)


# pytest tests/main/group/usecases/group/test_update.py::test_group_not_active_fail -v -s
@pytest.mark.asyncio
async def test_group_not_active_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_not_active: Group,
):
    uc = GroupUpdateUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(user=fxe_user_default, group_id=mock_group_get_not_active.id, update_obj=GroupUpdateDTO())


# pytest tests/main/group/usecases/group/test_update.py::test_group_user_permission_error -v -s
@pytest.mark.asyncio
async def test_group_user_permission_error(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_user_get_user: UserGroupDTO,
):
    uc = GroupUpdateUsecase(uow=uow)
    with pytest.raises(PermissionError):
        await uc(user=fxe_user_default, group_id=mock_group_get_default.id, update_obj=GroupUpdateDTO())
