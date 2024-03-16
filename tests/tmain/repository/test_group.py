from dataclasses import asdict
from datetime import datetime, timedelta

import pytest

from src.core.dto.group.group import GroupCreateDTO, GroupUpdateDTO
from src.core.dto.group.invite import GroupInviteUpdateDTO
from src.core.dto.m2m.user.group import UserGroupCreateDTO, UserGroupUpdateDTO
from src.core.dto.mock import MockObj
from src.core.entity.group import Group
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import (
    EntityNotChange,
    EntityNotCreated,
    EntityNotDeleted,
    EntityNotFound,
)
from src.core.interfaces.repository.group.group import (
    GroupFilter,
    GroupUserFilter,
    IRepositoryGroup,
)
from tests.dataloader import dataloader
from tests.utils import get_uuid


# pytest tests/tmain/repository/test_group.py::test_get_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_data",
    [
        dict(name="amogus", description="no desc", active=True, privacy=GroupPrivacyEnum.PUBLIC),
        dict(name="abobus", description="desc", active=False, privacy=GroupPrivacyEnum.PRIVATE),
    ],
)
async def test_get_ok(dl: dataloader, repo_group: IRepositoryGroup, create_data: dict):
    print()
    # Arrange
    group = await dl.group_loader.create(**create_data)
    # Act
    result = await repo_group.get(id=group.id)
    # Assert
    assert group.id == result.id
    assert group.name == create_data["name"] == result.name
    assert group.description == create_data["description"] == result.description
    assert group.active == create_data["active"] == result.active
    assert group.privacy == create_data["privacy"] == result.privacy


# pytest tests/tmain/repository/test_group.py::test_get_not_found -v -s
@pytest.mark.asyncio
async def test_get_not_found(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    await dl.group_loader.create()
    await dl.group_loader.create()
    model = await dl.group_loader.create()
    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_group.get(id=model.id + 1)


# pytest tests/tmain/repository/test_group.py::test_create_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_dto, asrt_dict",
    [
        (
            GroupCreateDTO(
                name="t1",
                description="123",
                active=True,
                privacy=GroupPrivacyEnum.PUBLIC,
            ),
            dict(name="t1", description="123", active=True, privacy=GroupPrivacyEnum.PUBLIC),
        ),
        (
            GroupCreateDTO(
                name="t2",
                description="124",
                active=False,
                privacy=GroupPrivacyEnum.PRIVATE,
            ),
            dict(name="t2", description="124", active=False, privacy=GroupPrivacyEnum.PRIVATE),
        ),
    ],
)
async def test_create_ok(dl: dataloader, repo_group: IRepositoryGroup, create_dto: GroupCreateDTO, asrt_dict: dict):
    # Arrange
    await dl.group_loader.create()
    await dl.group_loader.create()

    # Act
    group_create = await repo_group.create(obj=create_dto)

    asrt_dict["id"] = group_create.id
    group = await repo_group.get(id=group_create.id)
    # Assert
    assert asrt_dict == asdict(group_create)
    assert asrt_dict == asdict(group)

    await dl.rollback()


# pytest tests/tmain/repository/test_group.py::test_create_name_uniq_fail -v -s
@pytest.mark.asyncio
async def test_create_name_uniq_fail(
    dl: dataloader,
    repo_group: IRepositoryGroup,
):
    # Arrange
    name = "test_duplicate"
    await dl.group_loader.create(name=name)

    # Act & Assert
    with pytest.raises(EntityNotCreated) as exc:
        await repo_group.create(
            obj=GroupCreateDTO(name=name, privacy=GroupPrivacyEnum.PUBLIC, description="", active=True)
        )
        await dl.commit()
    assert "Uniq failed" in str(exc.value)


# pytest tests/tmain/repository/test_group.py::test_update_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_dto",
    [GroupUpdateDTO(name="changed", description="changed", active=False, privacy=GroupPrivacyEnum.PRIVATE)],
)
async def test_update_ok(dl: dataloader, repo_group: IRepositoryGroup, update_dto: GroupUpdateDTO):
    # Arrange
    target = await dl.group_loader.create(
        name="target", description="desc", active=True, privacy=GroupPrivacyEnum.PUBLIC
    )
    # Act
    updated = await repo_group.update(id=target.id, obj=update_dto)

    # Assert
    assert updated.id == target.id
    assert updated.name == update_dto.name
    assert updated.description == update_dto.description
    assert updated.active == update_dto.active
    assert updated.privacy == update_dto.privacy


# pytest tests/tmain/repository/test_group.py::test_update_name_uniq_error -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_one_dict, create_two_dict, update_dto",
    [
        (
            dict(name="target"),
            dict(name="target2"),
            GroupUpdateDTO(name="target"),
        )
    ],
)
async def test_update_name_uniq_error(
    dl: dataloader,
    repo_group: IRepositoryGroup,
    create_one_dict: dict,
    create_two_dict: dict,
    update_dto: GroupUpdateDTO,
):
    # Arrange
    await dl.group_loader.create(**create_one_dict)
    target_4change = await dl.group_loader.create(**create_two_dict)

    # Act & Assert
    with pytest.raises(EntityNotChange) as exc:
        await repo_group.update(id=target_4change.id, obj=update_dto)
    assert "Uniq failed" in str(exc.value)


# pytest tests/tmain/repository/test_group.py::test_update_not_found_error -v -s
@pytest.mark.asyncio
async def test_update_not_found_error(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    await dl.group_loader.create()
    last_created = await dl.group_loader.create()
    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_group.update(
            id=last_created.id + 1,
            obj=GroupUpdateDTO(name="changed"),
        )


async def _test_lst_user_id_param_first_variant(dl: dataloader):
    user = await dl.user_loader.create()
    user2 = await dl.user_loader.create()

    group = await dl.group_loader.create()
    group2 = await dl.group_loader.create()

    # user & user2 to group
    await dl.user_group_loader.create(user=user, group=group, role=GroupRoleEnum.USER)
    await dl.user_group_loader.create(user=user2, group=group, role=GroupRoleEnum.USER)

    # user2 to group 2
    await dl.user_group_loader.create(user=user2, group=group2, role=GroupRoleEnum.USER)

    return dict(filter_obj=GroupFilter(user_id=user.id), asrt_group_id_list=[group.id])


async def _test_lst_user_id_param_second_variant(dl: dataloader):
    user = await dl.user_loader.create()
    user2 = await dl.user_loader.create()

    group = await dl.group_loader.create()
    group2 = await dl.group_loader.create()

    # user & user2 to group
    await dl.user_group_loader.create(user=user, group=group, role=GroupRoleEnum.USER)
    await dl.user_group_loader.create(user=user2, group=group, role=GroupRoleEnum.USER)

    # user2 to group 2
    await dl.user_group_loader.create(user=user2, group=group2, role=GroupRoleEnum.USER)

    return dict(filter_obj=GroupFilter(user_id=user2.id), asrt_group_id_list=[group.id, group2.id])


async def _test_lst_user_id_param_third_variant(dl: dataloader):
    group = await dl.group_loader.create(active=True)
    group2 = await dl.group_loader.create(active=False)
    group3 = await dl.group_loader.create(active=True)

    return dict(filter_obj=GroupFilter(active=True), asrt_group_id_list=[group.id, group3.id])


# pytest tests/tmain/repository/test_group.py::test_lst_user_id -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [
        _test_lst_user_id_param_first_variant,
        _test_lst_user_id_param_second_variant,
        _test_lst_user_id_param_third_variant,
    ],
)
async def test_lst_user_id(dl: dataloader, repo_group: IRepositoryGroup, arrange_func):
    # Arrange
    arrange_result: dict = await arrange_func(dl)
    filter_obj = arrange_result["filter_obj"]
    asrt_group_id_list = arrange_result["asrt_group_id_list"]

    # Act
    group_list = await repo_group.lst(
        filter_obj=filter_obj,
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )

    # Assert
    group_id_list = [g.id for g in group_list]
    assert set(group_id_list) == set(asrt_group_id_list)


# pytest tests/tmain/repository/test_group.py::test_deactivate_ok -v -s
@pytest.mark.asyncio
async def test_deactivate_ok(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    group = await dl.group_loader.create(active=True)
    group2 = await dl.group_loader.create(active=True)

    # Act
    group_id = await repo_group.deactivate(
        id=group.id,
    )
    await dl.commit()

    # Assert
    assert group_id == group.id
    asrt_group = await repo_group.get(id=group.id)
    assert asrt_group.active == False
    # asrt for not changed
    asrt_group2 = await repo_group.get(id=group2.id)
    assert asrt_group2.active == True


# pytest tests/tmain/repository/test_group.py::test_deactivate_not_found_error -v -s
@pytest.mark.asyncio
async def test_deactivate_not_found_error(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    await dl.group_loader.create()
    last_created = await dl.group_loader.create()

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_group.deactivate(
            id=last_created.id + 1,
        )


# pytest tests/tmain/repository/test_group.py::test_code_get_ok -v -s
@pytest.mark.asyncio
async def test_code_get_ok(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    create_code = "shrekislive"
    expire_datetime = datetime.strptime("27.11.1999", "%d.%m.%Y")
    model = await dl.group_loader.create(code=create_code, code_expire_time=expire_datetime)

    # Act
    entity = await repo_group.code_get(id=model.id)

    # Assert
    assert entity.code == create_code
    assert entity.expire_time == expire_datetime


# pytest tests/tmain/repository/test_group.py::test_code_get_not_found -v -s
@pytest.mark.asyncio
async def test_code_get_not_found(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    expire_datetime = datetime.strptime("27.11.1999", "%d.%m.%Y")
    model = await dl.group_loader.create(code="shrekislive", code_expire_time=expire_datetime)

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_group.code_get(id=model.id + 1)  # select +1 on existed group model


# pytest tests/tmain/repository/test_group.py::test_code_set_ok -v -s
@pytest.mark.asyncio
async def test_code_set_ok(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    start_code = "shrekislive"
    start_expire_datetime = datetime.strptime("27.11.1999", "%d.%m.%Y")
    update_code = "oselislive"
    update_expire_datetime = datetime.strptime("28.11.1999", "%d.%m.%Y")
    start_model = await dl.group_loader.create(code=start_code, code_expire_time=start_expire_datetime)

    # Act
    entity_start = await repo_group.code_get(id=start_model.id)
    entity_update = await repo_group.code_set(
        id=start_model.id, obj=GroupInviteUpdateDTO(code=update_code, expire_time=update_expire_datetime)
    )

    # Assert
    assert entity_start.code == start_code
    assert entity_start.expire_time == start_expire_datetime
    assert entity_update.code == update_code
    assert entity_update.expire_time == update_expire_datetime


# pytest tests/tmain/repository/test_group.py::test_code_set_not_found -v -s
@pytest.mark.asyncio
async def test_code_set_not_found(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    expire_datetime = datetime.strptime("27.11.1999", "%d.%m.%Y")
    update_expire_datetime = datetime.strptime("28.11.1999", "%d.%m.%Y")
    model = await dl.group_loader.create(code="shrekislive", code_expire_time=expire_datetime)

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_group.code_set(
            id=model.id + 1, obj=GroupInviteUpdateDTO(code="something", expire_time=update_expire_datetime)
        )  # select +1 on existed group model


# pytest tests/tmain/repository/test_group.py::test_get_by_code_ok -v -s
@pytest.mark.asyncio
async def test_get_by_code_ok(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    code = "shrekislive"
    expire_datetime = datetime.now() + timedelta(days=5)
    model = await dl.group_loader.create(code=code, code_expire_time=expire_datetime)

    # Act
    entity = await repo_group.get_by_code(code=code)

    # Assert
    assert entity.id == model.id


# pytest tests/tmain/repository/test_group.py::test_get_by_code_not_found_code_not_exist -v -s
@pytest.mark.asyncio
async def test_get_by_code_not_found_code_not_exist(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    code = "shrekislive"
    expire_datetime = datetime.now() + timedelta(days=5)
    await dl.group_loader.create(code=code, code_expire_time=expire_datetime)

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_group.get_by_code(code="rnd")


# pytest tests/tmain/repository/test_group.py::test_get_by_code_not_found_expire_time -v -s
@pytest.mark.asyncio
async def test_get_by_code_not_found_expire_time(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    code = "shrekislive"
    expire_datetime = datetime.now() - timedelta(days=5)
    await dl.group_loader.create(code=code, code_expire_time=expire_datetime)

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_group.get_by_code(code=code)


# pytest tests/tmain/repository/test_group.py::test_user_add_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "role", [GroupRoleEnum.USER, GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER, GroupRoleEnum.BLOCKED]
)
async def test_user_add_ok(dl: dataloader, repo_group: IRepositoryGroup, role: GroupRoleEnum):
    # Arrange
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()

    # Act
    ug_entity = await repo_group.user_add(obj=UserGroupCreateDTO(user_id=user.id, group_id=group.id, role=role))

    # Assert
    assert ug_entity.user_id == user.id
    assert ug_entity.group_id == group.id
    assert ug_entity.role == role


# pytest tests/tmain/repository/test_group.py::test_user_add_uniq_fail -v -s
@pytest.mark.asyncio
async def test_user_add_uniq_fail(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    await dl.user_group_loader.create(user=user, group=group, role=GroupRoleEnum.USER)

    # Act
    with pytest.raises(EntityNotCreated) as e:
        await repo_group.user_add(obj=UserGroupCreateDTO(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER))

    # Assert
    assert "Uniq fail" in str(e.value)


async def _test_user_add_not_found_fk_fail_first_variant(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    return user.id, 1337


async def _test_user_add_not_found_fk_fail_second_variant(dl: dataloader) -> tuple[str, int]:
    group = await dl.group_loader.create()
    return get_uuid(), group.id


# pytest tests/tmain/repository/test_group.py::test_user_add_not_found_fk_fail -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func", [_test_user_add_not_found_fk_fail_first_variant, _test_user_add_not_found_fk_fail_second_variant]
)
async def test_user_add_not_found_fk_fail(dl: dataloader, repo_group: IRepositoryGroup, arrange_func):
    # Arrange
    user_id, group_id = await arrange_func(dl=dl)

    # Act
    with pytest.raises(EntityNotCreated) as e:
        await repo_group.user_add(obj=UserGroupCreateDTO(user_id=user_id, group_id=group_id, role=GroupRoleEnum.USER))

    # Assert
    assert "Not found fk" in str(e.value)


# pytest tests/tmain/repository/test_group.py::test_user_get_ok -v -s
@pytest.mark.asyncio
async def test_user_get_ok(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    role = GroupRoleEnum.USER
    ug = await dl.user_group_loader.create(user=user, group=group, role=role)

    # Act
    ug_entity = await repo_group.user_get(group_id=group.id, user_id=user.id)

    # Assert
    assert ug.group_id == ug_entity.group_id
    assert ug.user_id == ug_entity.user_id
    assert ug.role == role


async def _test_user_get_not_found_fail_first_variant(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    role = GroupRoleEnum.USER
    await dl.user_group_loader.create(user=user, group=group, role=role)
    return user.id, 1337


async def _test_user_get_not_found_fk_fail_second_variant(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    role = GroupRoleEnum.USER
    await dl.user_group_loader.create(user=user, group=group, role=role)
    return get_uuid(), 1337


# pytest tests/tmain/repository/test_group.py::test_user_get_not_found -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [_test_user_get_not_found_fail_first_variant, _test_user_get_not_found_fk_fail_second_variant],
)
async def test_user_get_not_found(dl: dataloader, repo_group: IRepositoryGroup, arrange_func):
    # Arrange
    user_id, group_id = await arrange_func(dl=dl)

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_group.user_get(group_id=group_id, user_id=user_id)


async def _test_user_get_list_first_variant(
    dl: dataloader,
) -> tuple[int, GroupUserFilter]:
    user = await dl.user_loader.create()
    user2 = await dl.user_loader.create()
    group = await dl.group_loader.create()
    role = GroupRoleEnum.USER
    await dl.user_group_loader.create(user=user, group=group, role=role)
    await dl.user_group_loader.create(user=user2, group=group, role=role)
    filter_obj = GroupUserFilter(user_id__in=[user.id, user2.id], role__in=[role])
    return group.id, filter_obj


async def _test_user_get_list_second_variant(dl: dataloader) -> tuple[int, GroupUserFilter]:
    user = await dl.user_loader.create()
    user2 = await dl.user_loader.create()
    group = await dl.group_loader.create()
    role = GroupRoleEnum.USER
    role2 = GroupRoleEnum.ADMIN
    await dl.user_group_loader.create(user=user, group=group, role=role)
    await dl.user_group_loader.create(user=user2, group=group, role=role2)
    filter_obj = GroupUserFilter(role__in=[role, role2])
    return group.id, filter_obj


async def _test_user_get_list_third_variant(dl: dataloader) -> tuple[int, GroupUserFilter]:
    user = await dl.user_loader.create()
    user2 = await dl.user_loader.create()
    group = await dl.group_loader.create()
    role = GroupRoleEnum.USER
    role2 = GroupRoleEnum.ADMIN
    await dl.user_group_loader.create(user=user, group=group, role=role)
    await dl.user_group_loader.create(user=user2, group=group, role=role2)
    filter_obj = GroupUserFilter(user_id__in=[user.id, user2.id])
    return group.id, filter_obj


# pytest tests/tmain/repository/test_group.py::test_user_get_list -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [_test_user_get_list_first_variant, _test_user_get_list_second_variant, _test_user_get_list_third_variant],
)
async def test_user_get_list(dl: dataloader, repo_group: IRepositoryGroup, arrange_func):
    # Arrange
    asrt_group_id, filter_obj = await arrange_func(dl=dl)
    filter_obj: GroupUserFilter = filter_obj

    # Act
    ug_list = await repo_group.user_list(id=asrt_group_id, filter_obj=filter_obj)

    # Assert
    group_id_set = set(ug.group_id for ug in ug_list)
    user_id_set = set(ug.user_id for ug in ug_list)
    role_set = set(ug.role for ug in ug_list)

    assert set([asrt_group_id]) == group_id_set
    if filter_obj.user_id__in is not None:
        assert set(filter_obj.user_id__in) == user_id_set
    if filter_obj.role__in is not None:
        assert set(filter_obj.role__in) == role_set


# pytest tests/tmain/repository/test_group.py::test_user_role_update_ok -v -s
@pytest.mark.asyncio
async def test_user_role_update_ok(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    role = GroupRoleEnum.USER
    new_role = GroupRoleEnum.ADMIN
    ug = await dl.user_group_loader.create(user=user, group=group, role=role)
    ug_role = ug.role

    # Act
    ug_entity_updated = await repo_group.user_role_update(
        user_id=user.id, group_id=group.id, obj=UserGroupUpdateDTO(role=new_role)
    )

    # Assert
    assert ug.group_id == ug_entity_updated.group_id
    assert ug.user_id == ug_entity_updated.user_id
    assert ug_role != ug_entity_updated.role
    assert ug_entity_updated.role == new_role


async def _test_user_role_update_not_found_fail_first_variant(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    role = GroupRoleEnum.USER
    await dl.user_group_loader.create(user=user, group=group, role=role)
    return user.id, 1337


async def _test_user_role_update_not_found_fk_fail_second_variant(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    role = GroupRoleEnum.USER
    await dl.user_group_loader.create(user=user, group=group, role=role)
    return get_uuid(), 1337


# pytest tests/tmain/repository/test_group.py::test_user_role_update_not_found -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [_test_user_role_update_not_found_fail_first_variant, _test_user_role_update_not_found_fk_fail_second_variant],
)
async def test_user_role_update_not_found(dl: dataloader, repo_group: IRepositoryGroup, arrange_func):
    # Arrange
    user_id, group_id = await arrange_func(dl=dl)

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_group.user_role_update(
            group_id=group_id, user_id=user_id, obj=UserGroupUpdateDTO(role=GroupRoleEnum.USER)
        )


# pytest tests/tmain/repository/test_group.py::test_user_remove_ok -v -s
@pytest.mark.asyncio
async def test_user_remove_ok(dl: dataloader, repo_group: IRepositoryGroup):
    # Arrange
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    role = GroupRoleEnum.USER
    await dl.user_group_loader.create(user=user, group=group, role=role)

    # Act
    status = await repo_group.user_remove(user_id=user.id, group_id=group.id)

    # Assert
    assert status is True


async def _test_user_remove_not_deleted_first_variant(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    role = GroupRoleEnum.USER
    await dl.user_group_loader.create(user=user, group=group, role=role)
    return user.id, 1337


async def _test_user_remove_not_deleted_second_variant(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    role = GroupRoleEnum.USER
    await dl.user_group_loader.create(user=user, group=group, role=role)
    return get_uuid(), 1337


# pytest tests/tmain/repository/test_group.py::test_user_remove_not_deleted -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [_test_user_remove_not_deleted_first_variant, _test_user_remove_not_deleted_second_variant],
)
async def test_user_remove_not_deleted(dl: dataloader, repo_group: IRepositoryGroup, arrange_func):
    # Arrange
    user_id, group_id = await arrange_func(dl=dl)

    # Act & Assert
    with pytest.raises(EntityNotDeleted):
        await repo_group.user_remove(group_id=group_id, user_id=user_id)
