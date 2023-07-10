import pytest

from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.community.community_join_by_code import (
    CommunityJoinByCodeUsecase,
)
from tests.fixtures.community.usecase.community import (
    mock_community_get_by_code,
    mock_community_get_by_code_not_active,
)
from tests.fixtures.community.usecase.user import mock_community_user_add_user
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/community/usecases/community/test_join_by_code.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_by_code: Community,
    mock_community_user_add_user: UserCommunityDTO,
):
    uc = CommunityJoinByCodeUsecase(uow=uow)
    res = await uc(user=fxe_user_default, code="aboba")
    community_user = res.item
    assert community_user.user_id == mock_community_user_add_user.user_id
    assert community_user.community_id == mock_community_user_add_user.community_id
    assert community_user.role == mock_community_user_add_user.role


# pytest tests/main/community/usecases/community/test_join_by_code.py::test_community_not_active -v -s
@pytest.mark.asyncio
async def test_community_not_active(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_by_code_not_active: Community,
    mock_community_user_add_user: UserCommunityDTO,
):
    uc = CommunityJoinByCodeUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(user=fxe_user_default, code="aboba")
