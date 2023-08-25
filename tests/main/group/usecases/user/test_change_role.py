import pytest

from src.core.dto.m2m.user.group import UserGroupDTO, UserGroupUpdateDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive, EntityNotFound, PermissionError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_change_user_role import GroupChangeUserRoleUsecase
from tests.fixtures.group.usecase.group import (
    mock_group_get_default,
    mock_group_get_not_active,
)
from tests.fixtures.group.usecase.user import (
    mock_group_user_list_ret_admin_superuser,
    mock_group_user_list_ret_not_found_current_user,
    mock_group_user_list_ret_superuser_admin,
    mock_group_user_list_ret_user_user,
    mock_group_user_update_role,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/group/usecases/user/test_change_role.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_user_list_ret_superuser_admin: list[UserGroupDTO],
    mock_group_user_update_role: UserGroupDTO,
):
    current_user = mock_group_user_list_ret_superuser_admin[0]
    fxe_user_default.id = current_user.user_id
    target_user = mock_group_user_list_ret_superuser_admin[1]
    uc = GroupChangeUserRoleUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        group_id=mock_group_get_default.id,
        user_id=target_user.user_id,
        update_obj=UserGroupUpdateDTO(role=GroupRoleEnum.SUPERUSER),
    )
    group_user = res.item
    assert isinstance(group_user, UserGroupDTO)


# pytest tests/main/group/usecases/user/test_change_role.py::test_group_not_active_fail -v -s
@pytest.mark.asyncio
async def test_group_not_active_fail(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_not_active: Group,
):
    uc = GroupChangeUserRoleUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(
            user=fxe_user_default,
            group_id=1,
            user_id=1,
            update_obj=UserGroupUpdateDTO(role=GroupRoleEnum.SUPERUSER),
        )


# pytest tests/main/group/usecases/user/test_change_role.py::test_not_found_current_user -v -s
@pytest.mark.asyncio
async def test_not_found_current_user(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_user_list_ret_not_found_current_user: list[UserGroupDTO],
):
    fxe_user_default.id = -1
    target_user = mock_group_user_list_ret_not_found_current_user[0]
    uc = GroupChangeUserRoleUsecase(uow=uow)
    with pytest.raises(EntityNotFound, match="Not found current user user_id=-1"):
        await uc(
            user=fxe_user_default,
            group_id=1,
            user_id=target_user.user_id,
            update_obj=UserGroupUpdateDTO(role=GroupRoleEnum.SUPERUSER),
        )


# pytest tests/main/group/usecases/user/test_change_role.py::test_not_found_target_user -v -s
@pytest.mark.asyncio
async def test_not_found_target_user(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_user_list_ret_not_found_current_user: list[UserGroupDTO],
):
    uc = GroupChangeUserRoleUsecase(uow=uow)
    with pytest.raises(EntityNotFound, match="Not found target user user_id=-1"):
        await uc(
            user=fxe_user_default,
            group_id=1,
            user_id=-1,
            update_obj=UserGroupUpdateDTO(role=GroupRoleEnum.SUPERUSER),
        )


# pytest tests/main/group/usecases/user/test_change_role.py::test_permission_current_user_error -v -s
@pytest.mark.asyncio
async def test_permission_current_user_error(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_user_list_ret_user_user: list[UserGroupDTO],
):
    current_user = mock_group_user_list_ret_user_user[0]
    target_user = mock_group_user_list_ret_user_user[1]
    uc = GroupChangeUserRoleUsecase(uow=uow)
    with pytest.raises(PermissionError, match="current user is not administrator"):
        await uc(
            user=fxe_user_default,
            group_id=mock_group_get_default.id,
            user_id=target_user.user_id,
            update_obj=UserGroupUpdateDTO(role=GroupRoleEnum.SUPERUSER),
        )


# pytest tests/main/group/usecases/user/test_change_role.py::test_permission_error -v -s
@pytest.mark.asyncio
async def test_permission_error(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_user_list_ret_admin_superuser: list[UserGroupDTO],
):
    current_user = mock_group_user_list_ret_admin_superuser[0]
    fxe_user_default.id = current_user.user_id
    target_user = mock_group_user_list_ret_admin_superuser[1]
    uc = GroupChangeUserRoleUsecase(uow=uow)
    with pytest.raises(PermissionError, match="current user is not superuser"):
        await uc(
            user=fxe_user_default,
            group_id=mock_group_get_default.id,
            user_id=target_user.user_id,
            update_obj=UserGroupUpdateDTO(role=GroupRoleEnum.SUPERUSER),
        )
