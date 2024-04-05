from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from src.core.dto.group.group import GroupCreateDTO, GroupUpdateDTO
from src.core.dto.m2m.user.group import UserGroupUpdateDTO
from src.core.dto.utils import IterableObj
from src.core.entity.user import User
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import (
    EntityNotActive,
    EntityNotFound,
    LogicError,
    PermissionError,
    PrivacyError,
)
from src.core.interfaces.repository.group.group import (
    GroupFilter,
    GroupUserFilter,
    SortingGroupObj,
)
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_change_user_role import GroupChangeUserRoleUsecase
from src.core.usecases.group.group_create import GroupCreateUsecase
from src.core.usecases.group.group_delete import GroupDeleteUsecase
from src.core.usecases.group.group_get import GroupGetUsecase
from src.core.usecases.group.group_get_invite_link import GroupGetInviteCodeUsecase
from src.core.usecases.group.group_join_by_code import GroupJoinByCodeUsecase
from src.core.usecases.group.group_leave import GroupLeaveUsecase
from src.core.usecases.group.group_list import GroupListUsecase
from src.core.usecases.group.group_public_add_user import GroupPublicAddUserUsecase
from src.core.usecases.group.group_update import GroupUpdateUsecase
from src.core.usecases.group.group_user_list import GroupUserListUsecase
from src.data.models.group.group import GroupModel
from src.data.models.user.user import UserGroupModel
from src.data.repository.user import model_to_dto as user_model_to_dto
from tests.dataloader import dataloader


# pytest tests/tmain/usecase/test_group.py::test_private_group_get_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_role", [GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER, GroupRoleEnum.USER])
async def test_private_group_get_ok(uow: IUnitOfWork, dl: dataloader, arrange_role):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model, role=arrange_role, privacy=GroupPrivacyEnum.PRIVATE)
    await dl.group_loader.create()

    # Act
    uc = GroupGetUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id)

    # Assert
    assert res.item.id == group.id
    assert res.item.active == group.active
    assert res.item.description == group.description
    assert res.item.privacy == group.privacy


# pytest tests/tmain/usecase/test_group.py::test_public_group_get_user_in_group_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_role", [GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER, GroupRoleEnum.USER])
async def test_public_group_get_user_in_group_ok(uow: IUnitOfWork, dl: dataloader, arrange_role):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model, role=arrange_role)
    await dl.group_loader.create()

    # Act
    uc = GroupGetUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id)

    # Assert
    assert res.item.id == group.id
    assert res.item.active == group.active
    assert res.item.description == group.description
    assert res.item.privacy == group.privacy


# pytest tests/tmain/usecase/test_group.py::test_public_group_get_user_not_in_group_ok -v -s
@pytest.mark.asyncio
async def test_public_group_get_user_not_in_group_ok(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group()
    await dl.group_loader.create()

    # Act
    uc = GroupGetUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id)

    # Assert
    assert res.item.id == group.id
    assert res.item.active == group.active
    assert res.item.description == group.description
    assert res.item.privacy == group.privacy


# pytest tests/tmain/usecase/test_group.py::test_group_get_group_not_active_error -v -s
@pytest.mark.asyncio
async def test_group_get_group_not_active_error(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.group_loader.create(active=False)
    await dl.group_loader.create()

    # Act
    uc = GroupGetUsecase(uow=uow)
    with pytest.raises(EntityNotActive) as e:
        await uc(user=user, group_id=group.id)

    # Assert
    assert f"{group.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_get_privacy_error -v -s
@pytest.mark.asyncio
async def test_group_get_privacy_error(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PRIVATE)
    await dl.group_loader.create()

    # Act
    uc = GroupGetUsecase(uow=uow)
    with pytest.raises(PrivacyError) as e:
        await uc(user=user, group_id=group.id)

    # Assert
    assert f"{group.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_get_permission_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_role", [GroupRoleEnum.ADMIN, GroupRoleEnum.BLOCKED, GroupRoleEnum.USER])
async def test_group_get_permission_error(uow: IUnitOfWork, dl: dataloader, arrange_role):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PRIVATE, active=False)

    await dl.user_group_loader.create(user=user_model, group=group, role=arrange_role)
    await dl.group_loader.create()

    # Act
    uc = GroupGetUsecase(uow=uow)
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group.id)
    # Assert
    assert f"{user.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_create_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_obj",
    [
        GroupCreateDTO(name="private group", privacy=GroupPrivacyEnum.PRIVATE, description="some desc", active=True),
        GroupCreateDTO(name="public group", privacy=GroupPrivacyEnum.PUBLIC, description="some desc", active=True),
    ],
)
async def test_group_create_ok(uow: IUnitOfWork, dl: dataloader, create_obj: GroupCreateDTO):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)

    # Act
    uc = GroupCreateUsecase(uow=uow)
    res = await uc(user=user, create_obj=create_obj)

    # Assert
    assert res.item.active == create_obj.active
    assert res.item.description == create_obj.description
    assert res.item.name == create_obj.name
    assert res.item.privacy == create_obj.privacy

    await dl._delete(UserGroupModel, "group_id", res.item.id)
    await dl._delete(GroupModel, "id", res.item.id)


# pytest tests/tmain/usecase/test_group.py::test_group_delete_ok -v -s
@pytest.mark.asyncio
async def test_group_delete_ok(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model)
    await dl.group_loader.create(name="randname")

    # Act
    uc = GroupDeleteUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id)

    # Assert
    assert res.item == group.id


# pytest tests/tmain/usecase/test_group.py::test_group_delete_permission_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_role", [GroupRoleEnum.ADMIN, GroupRoleEnum.BLOCKED, GroupRoleEnum.USER])
async def test_group_delete_permission_error(uow: IUnitOfWork, dl: dataloader, arrange_role: GroupRoleEnum):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model, role=arrange_role)

    # Act
    uc = GroupDeleteUsecase(uow=uow)
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group.id)
    # Assert
    assert f"{user.username=}, group_id={group.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_delete_user_not_in_group -v -s
@pytest.mark.asyncio
async def test_group_delete_user_not_in_group(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group()

    # Act
    uc = GroupDeleteUsecase(uow=uow)
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group.id)
    # Assert
    assert f"{user.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_get_invite_link_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_role", [GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER])
async def test_group_get_invite_link_ok(uow: IUnitOfWork, dl: dataloader, arrange_role):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model, role=arrange_role)

    # Act
    uc = GroupGetInviteCodeUsecase(uow=uow, invite_expire_sec=200)
    res = await uc(user=user, group_id=group.id)

    # Assert
    assert isinstance(res.item.code, str)
    assert isinstance(res.item.expire_time, datetime)
    assert res.item.group_id == group.id


# pytest tests/tmain/usecase/test_group.py::test_group_get_invite_link_group_not_active_error -v -s
@pytest.mark.asyncio
async def test_group_get_invite_link_group_not_active_error(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model, active=False)

    # Act
    uc = GroupGetInviteCodeUsecase(uow=uow, invite_expire_sec=200)
    with pytest.raises(EntityNotActive) as e:
        await uc(user=user, group_id=group.id)

    # Assert
    assert f"{group.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_get_invite_link_permission_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_role", [GroupRoleEnum.BLOCKED, GroupRoleEnum.USER])
async def test_group_get_invite_link_permission_error(uow: IUnitOfWork, dl: dataloader, arrange_role: GroupRoleEnum):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model, role=arrange_role)

    # Act
    uc = GroupGetInviteCodeUsecase(uow=uow, invite_expire_sec=200)
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group.id)
    # Assert
    assert f"user_id={user.id}, group_id={group.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_change_user_role_group_not_active_error -v -s
@pytest.mark.asyncio
async def test_group_change_user_role_group_not_active_error(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    superuser_model = await dl.user_loader.create()
    superuser = user_model_to_dto(superuser_model)
    group = await dl.create_group(user=superuser_model, active=False)

    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    await dl.user_group_loader.create(user=user_model, group=group, role=GroupRoleEnum.USER)

    obj = UserGroupUpdateDTO(role=GroupRoleEnum.ADMIN)

    # Act
    uc = GroupChangeUserRoleUsecase(uow=uow)
    with pytest.raises(EntityNotActive) as e:
        await uc(user=superuser, group_id=group.id, user_id=user.id, update_obj=obj)
    # Assert
    assert f"{group.id=}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_change_user_role_current_user_not_in_group -v -s
@pytest.mark.asyncio
async def test_group_change_user_role_current_user_not_in_group(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    current_user_model = await dl.user_loader.create()
    current_user = user_model_to_dto(current_user_model)

    target_user_model = await dl.user_loader.create()
    target_user = user_model_to_dto(target_user_model)
    group = await dl.create_group(user=target_user_model, role=GroupRoleEnum.USER)

    obj = UserGroupUpdateDTO(role=GroupRoleEnum.ADMIN)

    # Act
    uc = GroupChangeUserRoleUsecase(uow=uow)
    with pytest.raises(EntityNotFound) as e:
        await uc(user=current_user, group_id=group.id, user_id=target_user.id, update_obj=obj)

    # Assert
    assert f"Not found current user user_id={current_user.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_change_user_role_target_user_not_in_group -v -s
@pytest.mark.asyncio
async def test_group_change_user_role_target_user_not_in_group(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    current_user_model = await dl.user_loader.create()
    current_user = user_model_to_dto(current_user_model)
    group = await dl.create_group(user=current_user_model)

    target_user_model = await dl.user_loader.create()

    obj = UserGroupUpdateDTO(role=GroupRoleEnum.ADMIN)

    # Act
    uc = GroupChangeUserRoleUsecase(uow=uow)
    with pytest.raises(EntityNotFound) as e:
        await uc(user=current_user, group_id=group.id, user_id=target_user_model.id, update_obj=obj)
    # Assert
    assert f"Not found target user user_id={target_user_model.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_change_user_role_current_user_is_not_administrator_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_role", [GroupRoleEnum.USER, GroupRoleEnum.BLOCKED])
async def test_group_change_user_role_current_user_is_not_administrator_error(
    uow: IUnitOfWork, dl: dataloader, arrange_role: GroupRoleEnum
):
    # Arrange
    current_user_model = await dl.user_loader.create()
    current_user = user_model_to_dto(current_user_model)
    group = await dl.create_group(user=current_user_model, role=arrange_role)

    target_user_model = await dl.user_loader.create()
    target_user = user_model_to_dto(target_user_model)
    await dl.user_group_loader.create(user=target_user_model, group=group, role=GroupRoleEnum.USER)

    obj = UserGroupUpdateDTO(role=GroupRoleEnum.ADMIN)

    # Act
    uc = GroupChangeUserRoleUsecase(uow=uow)
    with pytest.raises(PermissionError) as e:
        await uc(user=current_user, group_id=group.id, user_id=target_user.id, update_obj=obj)

    # Assert
    assert f"current user is not administrator: user_id={current_user.id}, group_id={group.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_change_user_role_current_user_is_not_superuser_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_role", [GroupRoleEnum.USER, GroupRoleEnum.BLOCKED, GroupRoleEnum.ADMIN])
async def test_group_change_user_role_current_user_is_not_superuser_error(
    uow: IUnitOfWork, dl: dataloader, arrange_role: GroupRoleEnum
):
    # Arrange
    current_user_model = await dl.user_loader.create()
    current_user = user_model_to_dto(current_user_model)
    group = await dl.create_group(user=current_user_model, role=arrange_role)

    target_user_model = await dl.user_loader.create()
    target_user = user_model_to_dto(target_user_model)
    await dl.user_group_loader.create(user=target_user_model, group=group, role=GroupRoleEnum.SUPERUSER)

    obj = UserGroupUpdateDTO(role=GroupRoleEnum.ADMIN)

    # Act
    uc = GroupChangeUserRoleUsecase(uow=uow)
    with pytest.raises(PermissionError) as e:
        await uc(user=current_user, group_id=group.id, user_id=target_user.id, update_obj=obj)

    # Assert
    assert f"current user is not superuser: user_id={current_user.id}, group_id={group.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_change_user_role_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_role", [GroupRoleEnum.SUPERUSER, GroupRoleEnum.BLOCKED, GroupRoleEnum.ADMIN])
async def test_group_change_user_role_ok(uow: IUnitOfWork, dl: dataloader, arrange_role: GroupRoleEnum):
    # Arrange
    current_user_model = await dl.user_loader.create()
    current_user = user_model_to_dto(current_user_model)
    group = await dl.create_group(user=current_user_model)

    target_user_model = await dl.user_loader.create()
    target_user = user_model_to_dto(target_user_model)
    await dl.user_group_loader.create(user=target_user_model, group=group, role=GroupRoleEnum.USER)

    obj = UserGroupUpdateDTO(role=arrange_role)

    fake_user = await dl.user_loader.create()
    await dl.user_group_loader.create(user=fake_user, group=group, role=arrange_role)

    # Act
    uc = GroupChangeUserRoleUsecase(uow=uow)
    res = await uc(user=current_user, group_id=group.id, user_id=target_user.id, update_obj=obj)

    # Assert
    assert res.item.group_id == group.id
    assert res.item.role == arrange_role
    assert res.item.user_id == target_user.id


# pytest tests/tmain/usecase/test_group.py::test_group_join_by_code_ok -v -s
@pytest.mark.asyncio
async def test_group_join_by_code_ok(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    code = uuid4().hex
    expire_datetime = datetime.now() + timedelta(days=5)
    group = await dl.group_loader.create(code=code, code_expire_time=expire_datetime)
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)

    await dl.user_loader.create()

    # Act
    uc = GroupJoinByCodeUsecase(uow=uow)
    res = await uc(user=user, code=code)

    # Assert
    assert res.item.group_id == group.id
    assert res.item.role == GroupRoleEnum.USER
    assert res.item.user_id == user.id

    await dl._delete(UserGroupModel, "user_id", pk=user.id)


# pytest tests/tmain/usecase/test_group.py::test_group_join_by_code_group_not_active -v -s
@pytest.mark.asyncio
async def test_group_join_by_code_group_not_active(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    code = uuid4().hex
    expire_datetime = datetime.now() + timedelta(days=5)
    group = await dl.group_loader.create(code=code, code_expire_time=expire_datetime, active=False)
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)

    # Act
    uc = GroupJoinByCodeUsecase(uow=uow)
    with pytest.raises(EntityNotActive) as e:
        await uc(user=user, code=code)
    # Assert
    assert f"group_id={group.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_leave_ok -v -s
@pytest.mark.asyncio
async def test_group_leave_ok(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model)

    fake_user_model = await dl.user_loader.create()
    await dl.user_group_loader.create(user=fake_user_model, group=group, role=GroupRoleEnum.SUPERUSER)

    # Act
    uc = GroupLeaveUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id)

    # Assert
    assert res.item == True


# pytest tests/tmain/usecase/test_group.py::test_group_leave_logic_error -v -s
@pytest.mark.asyncio
async def test_group_leave_logic_error(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model)

    fake_user = await dl.user_loader.create()
    await dl.user_group_loader.create(user=fake_user, group=group, role=GroupRoleEnum.USER)

    # Act
    uc = GroupLeaveUsecase(uow=uow)
    with pytest.raises(LogicError) as e:
        await uc(user=user, group_id=group.id)
    # Assert
    assert f"{user.id=}, group_id={group.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_list_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_count", [0, 10])
async def test_group_list_ok(uow: IUnitOfWork, dl: dataloader, arrange_count: int):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)
    group_list = await dl.create_group_list(count=arrange_count, active=True)

    # Act
    uc = GroupListUsecase(uow=uow)
    res = await uc(user=user, filter_obj=GroupFilter(), sorting_obj=SortingGroupObj(), iterable_obj=IterableObj())

    # Assert
    assert len(res.item) == len(group_list)
    assert isinstance(res.offset, int)
    assert isinstance(res.total, int)


# pytest tests/tmain/usecase/test_group.py::test_group_public_add_user_ok -v -s
@pytest.mark.asyncio
async def test_group_public_add_user_ok(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)
    group = await dl.group_loader.create(name="band")

    await dl.user_loader.create()
    await dl.group_loader.create(name="group")

    # Act
    uc = GroupPublicAddUserUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id)

    # Assert
    assert res.item.group_id == group.id
    assert res.item.role == GroupRoleEnum.USER
    assert res.item.user_id == user.id

    await dl._delete(UserGroupModel, "user_id", res.item.user_id)


# pytest tests/tmain/usecase/test_group.py::test_not_active_group_add_user_error -v -s
@pytest.mark.asyncio
async def test_not_active_group_add_user_error(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model, active=False)

    # Act
    uc = GroupPublicAddUserUsecase(uow=uow)
    with pytest.raises(EntityNotActive) as e:
        await uc(user=user, group_id=group.id)

    # Assert
    assert f"{group.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_private_group_add_user_error -v -s
@pytest.mark.asyncio
async def test_private_group_add_user_error(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model, privacy=GroupPrivacyEnum.PRIVATE)

    # Act
    uc = GroupPublicAddUserUsecase(uow=uow)
    with pytest.raises(PrivacyError) as e:
        await uc(user=user, group_id=group.id)

    # Assert
    assert f"{group.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_update_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_update_obj",
    [
        GroupUpdateDTO(name="im an ogre", description="arrrr", privacy=GroupPrivacyEnum.PRIVATE, active=True),
        GroupUpdateDTO(name="donkey", description="dragonfucker", privacy=GroupPrivacyEnum.PUBLIC, active=False),
    ],
)
async def test_group_update_ok(uow: IUnitOfWork, dl: dataloader, arrange_update_obj: GroupUpdateDTO):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model)

    # Act
    uc = GroupUpdateUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id, update_obj=arrange_update_obj)

    # Assert
    assert res.item.id == group.id
    assert res.item.active == arrange_update_obj.active
    assert res.item.description == arrange_update_obj.description
    assert res.item.name == arrange_update_obj.name
    assert res.item.privacy == arrange_update_obj.privacy


# pytest tests/tmain/usecase/test_group.py::test_not_active_group_user_list_error -v -s
@pytest.mark.asyncio
async def test_not_active_group_user_list_error(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model, active=False)

    # Act
    uc = GroupUserListUsecase(uow=uow)
    with pytest.raises(EntityNotActive) as e:
        await uc(user=user, group_id=group.id, filter_obj=GroupUserFilter())
    # Assert
    assert f"{group.id}" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_group_user_list_user_blocked_error -v -s
@pytest.mark.asyncio
async def test_group_user_list_user_blocked_error(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model, role=GroupRoleEnum.BLOCKED)

    # Act
    uc = GroupUserListUsecase(uow=uow)
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group.id, filter_obj=GroupUserFilter())
    # Assert
    assert f"{user.id=} is BLOCKED" in str(e.value)


async def _arrange_group_user_list_user_not_in_group(dl: dataloader) -> tuple[User, GroupModel]:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group()

    return user, group


async def _arrange_group_user_list_user_not_in_priveleged_roles(dl: dataloader) -> tuple[User, GroupModel]:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model, role=GroupRoleEnum.USER)

    return user, group


# pytest tests/tmain/usecase/test_group.py::test_public_group_user_list_blocked_role_in_filter_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func", [_arrange_group_user_list_user_not_in_group, _arrange_group_user_list_user_not_in_priveleged_roles]
)
async def test_public_group_user_list_blocked_role_in_filter_error(uow: IUnitOfWork, dl: dataloader, arrange_func):
    # Arrange
    user, group = await arrange_func(dl=dl)
    filter_obj = GroupUserFilter(role__in=[GroupRoleEnum.BLOCKED])

    # Act
    uc = GroupUserListUsecase(uow=uow)
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group.id, filter_obj=filter_obj)
    # Assert
    assert "User cannot see BLOCKED users in public group" in str(e.value)


# async def _arrange_public_group_user_list_first_varriant(dl: dataloader) -> tuple[User, GroupModel, set[str]]:
#     user, group = await _arrange_group_user_list_user_not_in_group(dl=dl)
#     group_user_list = await dl.create_group_user_list_random(group=group)
#     group_user_id_set = {
#         group_user.user_id for group_user in group_user_list if group_user.role != GroupRoleEnum.BLOCKED
#     }

#     return user, group, group_user_id_set


# async def _arrange_public_group_user_list_second_varriant(dl: dataloader) -> tuple[User, GroupModel, set[str]]:
#     user, group = await _arrange_group_user_list_user_not_in_priveleged_roles(dl=dl)
#     group_user_list = await dl.create_group_user_list_random(group=group)
#     group_user_id_set = {
#         group_user.user_id for group_user in group_user_list if group_user.role != GroupRoleEnum.BLOCKED
#     }

#     group_user_id_set.add(user.id)

#     return user, group, group_user_id_set


# pytest tests/tmain/usecase/test_group.py::test_public_group_user_list_ok -v -s
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "arrange_func", [_arrange_public_group_user_list_first_varriant, _arrange_public_group_user_list_second_varriant]
# )
# async def test_public_group_user_list_ok(uow: IUnitOfWork, dl: dataloader, arrange_func):
#     # Arrange
#     user, group, arrange_user_id_set = await arrange_func(dl=dl)

#     # Act
#     uc = GroupUserListUsecase(uow=uow)
#     res = await uc(user=user, group_id=group.id, filter_obj=GroupUserFilter())

#     res_user_id_set = {group_user.user_id for group_user in res.items}

#     # # Assert
#     assert res_user_id_set == arrange_user_id_set


# pytest tests/tmain/usecase/test_group.py::test_private_group_user_list_blocked_role_in_filter_error -v -s
@pytest.mark.asyncio
async def test_private_group_user_list_blocked_role_in_filter_error(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(user=user_model, privacy=GroupPrivacyEnum.PRIVATE, role=GroupRoleEnum.USER)

    filter_obj = GroupUserFilter(role__in=[GroupRoleEnum.BLOCKED])

    # Act
    uc = GroupUserListUsecase(uow=uow)
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group.id, filter_obj=filter_obj)
    # Assert
    assert f"cannot see BLOCKED users in private group" in str(e.value)


# pytest tests/tmain/usecase/test_group.py::test_private_group_user_list_user_not_in_group_error -v -s
@pytest.mark.asyncio
async def test_private_group_user_list_user_not_in_group_error(uow: IUnitOfWork, dl: dataloader):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(user_model)
    group = await dl.create_group(privacy=GroupPrivacyEnum.PRIVATE)

    # Act
    uc = GroupUserListUsecase(uow=uow)
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group.id, filter_obj=GroupUserFilter())
    # Assert
    assert "User outside a private group" in str(e.value)


# async def _arrange_private_group_user_list_user_role(dl: dataloader) -> tuple[User, GroupModel, set[str]]:
#     user_model = await dl.user_loader.create()
#     user = user_model_to_dto(user_model)
#     group = await dl.create_group(user=user_model, role=GroupRoleEnum.USER, privacy=GroupPrivacyEnum.PRIVATE)
#     group_user_list = await dl.create_group_user_list_random(group=group)

#     group_user_id_set = {
#         group_user.user_id for group_user in group_user_list if group_user.role != GroupRoleEnum.BLOCKED
#     }
#     group_user_id_set.add(user.id)
#     return user, group, group_user_id_set


# async def _arrange_private_group_user_list_admin_role(dl: dataloader) -> tuple[User, GroupModel, set[str]]:
#     user_model = await dl.user_loader.create()
#     user = user_model_to_dto(user_model)
#     group = await dl.create_group(user=user_model, role=GroupRoleEnum.ADMIN, privacy=GroupPrivacyEnum.PRIVATE)
#     group_user_list = await dl.create_group_user_list_random(group=group)

#     group_user_id_set = {group_user.user_id for group_user in group_user_list}
#     group_user_id_set.add(user.id)
#     return user, group, group_user_id_set


# async def _arrange_private_group_user_list_superuser_role(dl: dataloader) -> tuple[User, GroupModel, set[str]]:
#     user_model = await dl.user_loader.create()
#     user = user_model_to_dto(user_model)
#     group = await dl.create_group(user=user_model, role=GroupRoleEnum.SUPERUSER, privacy=GroupPrivacyEnum.PRIVATE)
#     group_user_list = await dl.create_group_user_list_random(group=group)

#     group_user_id_set = {group_user.user_id for group_user in group_user_list}
#     group_user_id_set.add(user.id)
#     return user, group, group_user_id_set


# pytest tests/tmain/usecase/test_group.py::test_private_group_user_list_ok -v -s
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "arrange_func",
#     [
#         _arrange_private_group_user_list_user_role,
#         _arrange_private_group_user_list_admin_role,
#         _arrange_private_group_user_list_superuser_role,
#     ],
# )
# async def test_private_group_user_list_ok(uow: IUnitOfWork, dl: dataloader, arrange_func):
#     # Arrange
#     user, group, arrange_group_user_id_set = await arrange_func(dl=dl)

#     # Act
#     uc = GroupUserListUsecase(uow=uow)
#     res = await uc(user=user, group_id=group.id, filter_obj=GroupUserFilter())

#     res_group_user_id_set = {group_user.user_id for group_user in res.items}

#     # Assert
#     assert res_group_user_id_set == arrange_group_user_id_set
