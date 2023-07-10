import pytest

from src.core.dto.m2m.user.community import UserCommunityDTO, UserCommunityUpdateDTO
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.base import EntityNotActive, EntityNotFound, PermissionError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.community.community_change_user_role import (
    CommunityChangeUserRoleUsecase,
)
from tests.fixtures.community.usecase.community import (
    mock_community_get_default,
    mock_community_get_not_active,
)
from tests.fixtures.community.usecase.user import (
    mock_community_user_list_ret_admin_superuser,
    mock_community_user_list_ret_not_found_current_user,
    mock_community_user_list_ret_superuser_admin,
    mock_community_user_list_ret_user_user,
    mock_community_user_update_role,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/community/usecases/user/test_change_role.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_default: Community,
    mock_community_user_list_ret_superuser_admin: list[UserCommunityDTO],
    mock_community_user_update_role: UserCommunityDTO,
):
    current_user = mock_community_user_list_ret_superuser_admin[0]
    fxe_user_default.id = current_user.user_id
    target_user = mock_community_user_list_ret_superuser_admin[1]
    uc = CommunityChangeUserRoleUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        community_id=mock_community_get_default.id,
        user_id=target_user.user_id,
        update_obj=UserCommunityUpdateDTO(role=CommunityRoleEnum.SUPERUSER),
    )
    community_user = res.item
    assert isinstance(community_user, UserCommunityDTO)


# pytest tests/main/community/usecases/user/test_change_role.py::test_community_not_active_fail -v -s
@pytest.mark.asyncio
async def test_community_not_active_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_not_active: Community,
):
    uc = CommunityChangeUserRoleUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(
            user=fxe_user_default,
            community_id=1,
            user_id=1,
            update_obj=UserCommunityUpdateDTO(role=CommunityRoleEnum.SUPERUSER),
        )


# pytest tests/main/community/usecases/user/test_change_role.py::test_not_found_current_user -v -s
@pytest.mark.asyncio
async def test_not_found_current_user(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_default: Community,
    mock_community_user_list_ret_not_found_current_user: list[UserCommunityDTO],
):
    fxe_user_default.id = -1
    target_user = mock_community_user_list_ret_not_found_current_user[0]
    uc = CommunityChangeUserRoleUsecase(uow=uow)
    with pytest.raises(EntityNotFound, match="Not found current user user_id=-1"):
        await uc(
            user=fxe_user_default,
            community_id=1,
            user_id=target_user.user_id,
            update_obj=UserCommunityUpdateDTO(role=CommunityRoleEnum.SUPERUSER),
        )


# pytest tests/main/community/usecases/user/test_change_role.py::test_not_found_target_user -v -s
@pytest.mark.asyncio
async def test_not_found_target_user(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_default: Community,
    mock_community_user_list_ret_not_found_current_user: list[UserCommunityDTO],
):
    uc = CommunityChangeUserRoleUsecase(uow=uow)
    with pytest.raises(EntityNotFound, match="Not found target user user_id=-1"):
        await uc(
            user=fxe_user_default,
            community_id=1,
            user_id=-1,
            update_obj=UserCommunityUpdateDTO(role=CommunityRoleEnum.SUPERUSER),
        )


# pytest tests/main/community/usecases/user/test_change_role.py::test_permission_current_user_error -v -s
@pytest.mark.asyncio
async def test_permission_current_user_error(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_default: Community,
    mock_community_user_list_ret_user_user: list[UserCommunityDTO],
):
    current_user = mock_community_user_list_ret_user_user[0]
    target_user = mock_community_user_list_ret_user_user[1]
    uc = CommunityChangeUserRoleUsecase(uow=uow)
    with pytest.raises(PermissionError, match="current user is not administrator"):
        await uc(
            user=fxe_user_default,
            community_id=mock_community_get_default.id,
            user_id=target_user.user_id,
            update_obj=UserCommunityUpdateDTO(role=CommunityRoleEnum.SUPERUSER),
        )


# pytest tests/main/community/usecases/user/test_change_role.py::test_permission_error -v -s
@pytest.mark.asyncio
async def test_permission_error(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_default: Community,
    mock_community_user_list_ret_admin_superuser: list[UserCommunityDTO],
):
    current_user = mock_community_user_list_ret_admin_superuser[0]
    fxe_user_default.id = current_user.user_id
    target_user = mock_community_user_list_ret_admin_superuser[1]
    uc = CommunityChangeUserRoleUsecase(uow=uow)
    with pytest.raises(PermissionError, match="current user is not superuser"):
        await uc(
            user=fxe_user_default,
            community_id=mock_community_get_default.id,
            user_id=target_user.user_id,
            update_obj=UserCommunityUpdateDTO(role=CommunityRoleEnum.SUPERUSER),
        )
