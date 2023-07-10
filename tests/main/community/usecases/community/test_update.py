import pytest

from src.core.dto.community.community import CommunityCreateDTO, CommunityUpdateDTO
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive, PermissionError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.community.community_update import CommunityUpdateUsecase
from tests.fixtures.community.usecase.community import (
    mock_community_get_default,
    mock_community_get_not_active,
    mock_community_update,
)
from tests.fixtures.community.usecase.user import (
    mock_community_user_get_default,
    mock_community_user_get_user,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/community/usecases/community/test_update.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_default: Community,
    mock_community_update: Community,
    mock_community_user_get_default: UserCommunityDTO,
):
    uc = CommunityUpdateUsecase(uow=uow)
    res = await uc(user=fxe_user_default, community_id=mock_community_get_default.id, update_obj=CommunityUpdateDTO())
    # active filter was changed to true
    community = res.item
    assert isinstance(community, Community)


# pytest tests/main/community/usecases/community/test_update.py::test_community_not_active_fail -v -s
@pytest.mark.asyncio
async def test_community_not_active_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_not_active: Community,
):
    uc = CommunityUpdateUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(user=fxe_user_default, community_id=mock_community_get_not_active.id, update_obj=CommunityUpdateDTO())


# pytest tests/main/community/usecases/community/test_update.py::test_community_user_permission_error -v -s
@pytest.mark.asyncio
async def test_community_user_permission_error(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_default: Community,
    mock_community_user_get_user: UserCommunityDTO,
):
    uc = CommunityUpdateUsecase(uow=uow)
    with pytest.raises(PermissionError):
        await uc(user=fxe_user_default, community_id=mock_community_get_default.id, update_obj=CommunityUpdateDTO())
