import pytest

from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.base import EntityNotActive, PrivacyError
from src.core.exception.user import PermissionError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.community.community_public_add_user import (
    CommunityPublicAddUserUsecase,
)
from tests.fixtures.community.usecase.community import (
    mock_community_get_active_private,
    mock_community_get_default,
    mock_community_get_not_active,
)
from tests.fixtures.community.usecase.user import mock_community_user_add_user
from tests.fixtures.const import DEFAULT_TEST_USECASE_COMMUNITY_ID
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/community/usecases/user/test_public_user_add.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_default: Community,
    mock_community_user_add_user: UserCommunityDTO,
):
    uc = CommunityPublicAddUserUsecase(uow=uow)
    res = await uc(user=fxe_user_default, community_id=mock_community_get_default.id)
    community_user = res.item
    assert isinstance(community_user, UserCommunityDTO)
    assert community_user.role == CommunityRoleEnum.USER


# pytest tests/main/community/usecases/user/test_public_user_add.py::test_community_not_active_fail -v -s
@pytest.mark.asyncio
async def test_community_not_active_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_not_active: Community,
):
    uc = CommunityPublicAddUserUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(user=fxe_user_default, community_id=mock_community_get_not_active.id)


# pytest tests/main/community/usecases/user/test_public_user_add.py::test_community_not_public_fail -v -s
@pytest.mark.asyncio
async def test_community_not_public_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_active_private: Community,
):
    uc = CommunityPublicAddUserUsecase(uow=uow)
    with pytest.raises(PrivacyError):
        await uc(user=fxe_user_default, community_id=mock_community_get_active_private.id)
