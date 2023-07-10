from datetime import datetime, timedelta

import pytest

from src.core.dto.community.invite import CommunityInviteDTO
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive, PermissionError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.community.community_get_invite_link import (
    CommunityGetInviteCodeUsecase,
)
from tests.fixtures.community.usecase.community import (
    mock_community_code_get_code_none,
    mock_community_code_get_default,
    mock_community_code_set_default,
    mock_community_get_default,
    mock_community_get_not_active,
)
from tests.fixtures.community.usecase.user import (
    mock_community_user_get_admin,
    mock_community_user_get_user,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/community/usecases/other/get_invite_link.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_default: Community,
    mock_community_user_get_admin: UserCommunityDTO,
    mock_community_code_get_default: CommunityInviteDTO,
    mock_community_code_set_default,
):
    uc = CommunityGetInviteCodeUsecase(uow=uow, invite_expire_sec=5)
    res = await uc(user=fxe_user_default, community_id=mock_community_get_default.id)
    invite = res.item
    assert isinstance(invite, CommunityInviteDTO)


# pytest tests/main/community/usecases/other/get_invite_link.py::test_code_get_empty -v -s
@pytest.mark.asyncio
async def test_code_get_empty(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_default: Community,
    mock_community_user_get_admin: UserCommunityDTO,
    mock_community_code_get_code_none: CommunityInviteDTO,
    mock_community_code_set_default,
):
    uc = CommunityGetInviteCodeUsecase(uow=uow, invite_expire_sec=5)
    res = await uc(user=fxe_user_default, community_id=mock_community_get_default.id)
    invite = res.item
    assert isinstance(invite, CommunityInviteDTO)
    assert invite.code is not None
    assert isinstance(invite.expire_time, datetime)
    current_time = datetime.utcnow()
    assert invite.expire_time > current_time
    delta = invite.expire_time - current_time
    assert delta < timedelta(seconds=5)
    assert delta > timedelta(seconds=4)


# pytest tests/main/community/usecases/other/get_invite_link.py::test_community_not_active_fail -v -s
@pytest.mark.asyncio
async def test_community_not_active_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_not_active: Community,
):
    uc = CommunityGetInviteCodeUsecase(uow=uow, invite_expire_sec=5)
    with pytest.raises(EntityNotActive):
        await uc(user=fxe_user_default, community_id=mock_community_get_not_active.id)


# pytest tests/main/community/usecases/other/get_invite_link.py::test_permission_fail -v -s
@pytest.mark.asyncio
async def test_permission_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_default: Community,
    mock_community_user_get_user: UserCommunityDTO,
):
    uc = CommunityGetInviteCodeUsecase(uow=uow, invite_expire_sec=5)
    with pytest.raises(PermissionError):
        await uc(user=fxe_user_default, community_id=mock_community_get_default.id)
