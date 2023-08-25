from datetime import datetime, timedelta

import pytest

from src.core.dto.group.invite import GroupInviteDTO
from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive, PermissionError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_get_invite_link import GroupGetInviteCodeUsecase
from tests.fixtures.group.usecase.group import (
    mock_group_code_get_code_none,
    mock_group_code_get_default,
    mock_group_code_set_default,
    mock_group_get_default,
    mock_group_get_not_active,
)
from tests.fixtures.group.usecase.user import (
    mock_group_user_get_admin,
    mock_group_user_get_user,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/group/usecases/other/get_invite_link.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_user_get_admin: UserGroupDTO,
    mock_group_code_get_default: GroupInviteDTO,
    mock_group_code_set_default,
):
    uc = GroupGetInviteCodeUsecase(uow=uow, invite_expire_sec=5)
    res = await uc(user=fxe_user_default, group_id=mock_group_get_default.id)
    invite = res.item
    assert isinstance(invite, GroupInviteDTO)


# pytest tests/main/group/usecases/other/get_invite_link.py::test_code_get_empty -v -s
@pytest.mark.asyncio
async def test_code_get_empty(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_user_get_admin: UserGroupDTO,
    mock_group_code_get_code_none: GroupInviteDTO,
    mock_group_code_set_default,
):
    uc = GroupGetInviteCodeUsecase(uow=uow, invite_expire_sec=5)
    res = await uc(user=fxe_user_default, group_id=mock_group_get_default.id)
    invite = res.item
    assert isinstance(invite, GroupInviteDTO)
    assert invite.code is not None
    assert isinstance(invite.expire_time, datetime)
    current_time = datetime.utcnow()
    assert invite.expire_time > current_time
    delta = invite.expire_time - current_time
    assert delta < timedelta(seconds=5)
    assert delta > timedelta(seconds=4)


# pytest tests/main/group/usecases/other/get_invite_link.py::test_group_not_active_fail -v -s
@pytest.mark.asyncio
async def test_group_not_active_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_not_active: Group,
):
    uc = GroupGetInviteCodeUsecase(uow=uow, invite_expire_sec=5)
    with pytest.raises(EntityNotActive):
        await uc(user=fxe_user_default, group_id=mock_group_get_not_active.id)


# pytest tests/main/group/usecases/other/get_invite_link.py::test_permission_fail -v -s
@pytest.mark.asyncio
async def test_permission_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_user_get_user: UserGroupDTO,
):
    uc = GroupGetInviteCodeUsecase(uow=uow, invite_expire_sec=5)
    with pytest.raises(PermissionError):
        await uc(user=fxe_user_default, group_id=mock_group_get_default.id)
