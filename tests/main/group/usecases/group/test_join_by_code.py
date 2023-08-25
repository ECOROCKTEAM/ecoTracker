import pytest

from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_join_by_code import GroupJoinByCodeUsecase
from tests.fixtures.group.usecase.group import (
    mock_group_get_by_code,
    mock_group_get_by_code_not_active,
)
from tests.fixtures.group.usecase.user import mock_group_user_add_user
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/group/usecases/group/test_join_by_code.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_by_code: Group,
    mock_group_user_add_user: UserGroupDTO,
):
    uc = GroupJoinByCodeUsecase(uow=uow)
    res = await uc(user=fxe_user_default, code="aboba")
    group_user = res.item
    assert group_user.user_id == mock_group_user_add_user.user_id
    assert group_user.group_id == mock_group_user_add_user.group_id
    assert group_user.role == mock_group_user_add_user.role


# pytest tests/main/group/usecases/group/test_join_by_code.py::test_group_not_active -v -s
@pytest.mark.asyncio
async def test_group_not_active(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_by_code_not_active: Group,
    mock_group_user_add_user: UserGroupDTO,
):
    uc = GroupJoinByCodeUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(user=fxe_user_default, code="aboba")
