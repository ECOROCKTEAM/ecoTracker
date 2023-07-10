import pytest

from src.core.dto.community.community import CommunityCreateDTO
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.exception.base import LogicError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.community.community_leave import CommunityLeaveUsecase
from tests.fixtures.community.usecase.user import (
    mock_community_user_get_admin,
    mock_community_user_get_superuser,
    mock_community_user_get_user,
    mock_community_user_list_ret_superusers_1,
    mock_community_user_list_ret_superusers_10,
    mock_community_user_remove,
)
from tests.fixtures.const import DEFAULT_TEST_USECASE_COMMUNITY_ID
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/community/usecases/community/test_leave.py::test_ok_user -v -s
@pytest.mark.asyncio
async def test_ok_user(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_user_get_user: UserCommunityDTO,
    mock_community_user_remove: bool,
):
    uc = CommunityLeaveUsecase(uow=uow)
    res = await uc(user=fxe_user_default, community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID)
    check = res.item
    assert check is True


# pytest tests/main/community/usecases/community/test_leave.py::test_ok_admin -v -s
@pytest.mark.asyncio
async def test_ok_admin(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_user_get_admin: UserCommunityDTO,
    mock_community_user_remove: bool,
):
    uc = CommunityLeaveUsecase(uow=uow)
    res = await uc(user=fxe_user_default, community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID)
    check = res.item
    assert check is True


# pytest tests/main/community/usecases/community/test_leave.py::test_ok_superuser -v -s
@pytest.mark.asyncio
async def test_ok_superuser(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_user_get_superuser: UserCommunityDTO,
    mock_community_user_list_ret_superusers_10: list[UserCommunityDTO],
    mock_community_user_remove: bool,
):
    uc = CommunityLeaveUsecase(uow=uow)
    res = await uc(user=fxe_user_default, community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID)
    check = res.item
    assert check is True


# pytest tests/main/community/usecases/community/test_leave.py::test_superuser_fail -v -s
@pytest.mark.asyncio
async def test_superuser_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_user_get_superuser: UserCommunityDTO,
    mock_community_user_list_ret_superusers_1: list[UserCommunityDTO],
):
    uc = CommunityLeaveUsecase(uow=uow)
    with pytest.raises(LogicError):
        await uc(user=fxe_user_default, community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID)
