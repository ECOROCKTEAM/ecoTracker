from datetime import datetime
from random import randint

import pytest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive, EntityNotFound
from src.core.exception.user import PermissionError
from src.core.interfaces.repository.group.group import GroupUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_user_list import GroupUserListUsecase
from src.data.models.group.group import GroupModel
from src.data.models.user.user import UserGroupModel, UserModel
from tests.fixtures.const import DEFAULT_TEST_LANGUAGE
from tests.fixtures.group.db.model import fxm_group_default
from tests.fixtures.group.usecase.group import (
    mock_group_get_active_private,
    mock_group_get_default,
    mock_group_get_not_active,
)
from tests.fixtures.group.usecase.user import (
    mock_group_user_get_admin,
    mock_group_user_get_blocked,
    mock_group_user_get_user,
    mock_group_user_list_ret_admin_superuser,
    mock_group_user_list_ret_superusers_10,
    mock_group_user_list_ret_user_user,
)
from tests.fixtures.user.db.model import fxm_user_default
from tests.fixtures.user.usecase.entity import fxe_user_default
from tests.utils import get_random_str


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_private_group_user_not_in_group_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_private_group_user_not_in_group_error(
    mock_group_get_active_private: Group,
    uow: IUnitOfWork,
    fxe_user_default: User,
):
    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter()
    with pytest.raises(PermissionError) as e:
        await uc(user=fxe_user_default, group_id=mock_group_get_active_private.id, filter_obj=filter_obj)
    assert "User outside a private group cannot see any users in it" in str(e.value)


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_ok -v -s
@pytest.mark.asyncio
async def test_group_user_list_user_in_publick_group_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_user_list_ret_user_user: list[UserGroupDTO],
):
    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter()
    res = await uc(user=fxe_user_default, group_id=mock_group_get_default.id, filter_obj=filter_obj)
    assert mock_group_user_list_ret_user_user == res.items


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_not_in_group_with_blocked_filter_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_not_in_group_with_blocked_filter_error(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_default: Group,
    mock_group_user_list_ret_superusers_10: list[UserGroupDTO],
):
    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter(role__in=[GroupRoleEnum.BLOCKED])
    with pytest.raises(PermissionError) as e:
        await uc(user=fxe_user_default, group_id=mock_group_get_default.id, filter_obj=filter_obj)
    assert "User cannot see BLOCKED users in public group" in str(e.value)


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_user_in_group_with_blocked_filter_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_user_in_group_with_blocked_filter_error(
    uow: IUnitOfWork, fxe_user_default: User, mock_group_user_get_user: UserGroupDTO, mock_group_get_default: Group
):
    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter(role__in=[GroupRoleEnum.BLOCKED])
    with pytest.raises(PermissionError) as e:
        await uc(user=fxe_user_default, group_id=mock_group_get_default.id, filter_obj=filter_obj)
    assert "User cannot see BLOCKED users in public group" in str(e.value)


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_group_not_active_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_group_not_active_error(
    uow: IUnitOfWork, fxe_user_default: User, mock_group_get_not_active: Group
):
    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter()
    with pytest.raises(EntityNotActive) as e:
        await uc(user=fxe_user_default, group_id=mock_group_get_not_active.id, filter_obj=filter_obj)
    assert f"{mock_group_get_not_active.id}" in str(e.value)


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_group_none_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_group_none_error(
    uow: IUnitOfWork, fxe_user_default: User, mock_group_user_get_blocked: UserGroupDTO
):
    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter()
    group_id = 123
    with pytest.raises(EntityNotFound) as e:
        await uc(user=fxe_user_default, group_id=group_id, filter_obj=filter_obj)
    assert f"{group_id}" in str(e.value)


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_user_blocked_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_user_blocked_error(
    uow: IUnitOfWork, fxe_user_default: User, mock_group_get_default: Group, mock_group_user_get_blocked: UserGroupDTO
):
    uc = GroupUserListUsecase(uow=uow)
    filter_obj = GroupUserFilter()
    with pytest.raises(PermissionError) as e:
        await uc(user=fxe_user_default, group_id=mock_group_get_default.id, filter_obj=filter_obj)
    assert f"is BLOCKED" in str(e.value)


# pytest tests/main/group/usecases/user/test_user_list.py::test_group_user_list_ok -v -s
# @pytest.mark.asyncio
# async def test_group_user_list_ok(session: AsyncSession):
#     user_list = []
#     user_with_request = UserModel(
#         id="The Witcher", username="Geralt of Rivia", active=True, language=DEFAULT_TEST_LANGUAGE
#     )

#     user_list.append(user_with_request)
#     for _ in range(5):
#         random_user = UserModel(
#             id=get_random_str(), username=get_random_str(), active=True, language=DEFAULT_TEST_LANGUAGE
#         )
#         user_list.append(random_user)

#     group = GroupModel(
#         id=randint(1, 1984),
#         name="Test Group",
#         description="",
#         active=True,
#         privacy=GroupPrivacyEnum.PUBLIC,
#         code=get_random_str(),
#         code_expire_time=datetime.now(),
#     )

#     session.add_all([group, *user_list])
#     await session.commit()

#     user_group_list = []

#     for user in user_list:
#         user_group = UserGroupModel(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER)
#         user_group_list.append(user_group)

#     session.add_all([*user_group_list])
#     await session.commit()

#     for user_group in user_group_list:
#         await session.delete(user_group)
#         await session.commit()

#     for user in user_list:
#         await session.delete(user)
#         await session.commit()
#     await session.delete(group)
