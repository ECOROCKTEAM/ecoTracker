import pytest

from src.core.dto.community.community import CommunityCreateDTO
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.exception.user import PermissionError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.community.community_delete import CommunityDeleteUsecase
from tests.fixtures.community.usecase.community import mock_community_deactivate
from tests.fixtures.community.usecase.user import (
    mock_community_user_get_superuser,
    mock_community_user_get_user,
)
from tests.fixtures.const import DEFAULT_TEST_USECASE_COMMUNITY_ID
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/community/usecases/community/test_delete.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_deactivate: int,
    mock_community_user_get_superuser: UserCommunityDTO,
):
    uc = CommunityDeleteUsecase(uow=uow)
    res = await uc(user=fxe_user_default, community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID)
    community_id = res.item
    assert community_id == DEFAULT_TEST_USECASE_COMMUNITY_ID


# pytest tests/main/community/usecases/community/test_delete.py::test_user_not_superuser -v -s
@pytest.mark.asyncio
async def test_user_not_superuser(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_deactivate: int,
    mock_community_user_get_user: UserCommunityDTO,
):
    uc = CommunityDeleteUsecase(uow=uow)
    with pytest.raises(PermissionError):
        await uc(user=fxe_user_default, community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID)
