from dataclasses import asdict

import pytest
from click import group

from src.core.dto.group.group import GroupCreateDTO, GroupUpdateDTO
from src.core.dto.mock import MockObj
from src.core.entity.group import Group
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotChange, EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.group.group import GroupFilter, IRepositoryGroup
from tests.dataloader import dataloader


# pytest tests/tmain/test_group.py::test_tracking -v -s
@pytest.mark.asyncio
async def test_tracking(dl: dataloader):
    print()
    u = await dl.user_loader.create()
    u2 = await dl.user_loader.create()

    g = await dl.group_loader.create()
    g1 = await dl.group_loader.create()
    g2 = await dl.group_loader.create()

    await dl.user_group_loader.create(user_id=u.id, group_id=g.id, role=GroupRoleEnum.ADMIN)
    await dl.user_group_loader.create(user_id=u.id, group_id=g1.id, role=GroupRoleEnum.ADMIN)
    await dl.user_group_loader.create(user_id=u.id, group_id=g2.id, role=GroupRoleEnum.ADMIN)

    await dl.user_group_loader.create(user_id=u2.id, group_id=g.id, role=GroupRoleEnum.ADMIN)
    await dl.user_group_loader.create(user_id=u2.id, group_id=g1.id, role=GroupRoleEnum.ADMIN)


# pytest tests/tmain/test_group.py::test_get_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_data, asrt_result",
    [
        (
            dict(id=1337, name="amogus", description="no desc", active=True, privacy=GroupPrivacyEnum.PUBLIC),
            Group(id=1337, name="amogus", description="no desc", active=True, privacy=GroupPrivacyEnum.PUBLIC),
        ),
        (
            dict(id=1337, name="amogus", description="no desc", active=True, privacy=GroupPrivacyEnum.PUBLIC),
            Group(id=1337, name="amogus", description="no desc", active=True, privacy=GroupPrivacyEnum.PUBLIC),
        ),
    ],
)
async def test_get_ok(dl: dataloader, repo: IRepositoryGroup, create_data: dict, asrt_result: Group):
    print()
    # Arrange
    await dl.group_loader.create(**create_data)
    # Act
    result = await repo.get(id=1337)
    # Assert
    assert result == asrt_result


# pytest tests/tmain/test_group.py::test_get_not_found -v -s
@pytest.mark.asyncio
async def test_get_not_found(dl: dataloader, repo: IRepositoryGroup):
    # Arrange
    await dl.group_loader.create()
    await dl.group_loader.create()
    model = await dl.group_loader.create()
    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo.get(id=model.id + 1)


# pytest tests/tmain/test_group.py::test_create_ok -v -s
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
async def test_create_ok(dl: dataloader, repo: IRepositoryGroup, create_dto: GroupCreateDTO, asrt_dict: dict):
    # Arrange
    await dl.group_loader.create()
    await dl.group_loader.create()

    # Act
    group_create = await repo.create(obj=create_dto)

    asrt_dict["id"] = group_create.id
    group = await repo.get(id=group_create.id)
    # Assert
    assert asrt_dict == asdict(group_create)
    assert asrt_dict == asdict(group)

    await dl.rollback()


# pytest tests/tmain/test_group.py::test_create_name_uniq_fail -v -s
@pytest.mark.asyncio
async def test_create_name_uniq_fail(
    dl: dataloader,
    repo: IRepositoryGroup,
):
    # Arrange
    name = "test_duplicate"
    await dl.group_loader.create(name=name)

    # Act & Assert
    with pytest.raises(EntityNotCreated) as exc:
        await repo.create(obj=GroupCreateDTO(name=name, privacy=GroupPrivacyEnum.PUBLIC, description="", active=True))
        await dl.commit()
    assert "Uniq failed" in str(exc.value)


# pytest tests/tmain/test_group.py::test_update_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_dto",
    [GroupUpdateDTO(name="changed", description="changed", active=False, privacy=GroupPrivacyEnum.PRIVATE)],
)
async def test_update_ok(dl: dataloader, repo: IRepositoryGroup, update_dto: GroupUpdateDTO):
    # Arrange
    target = await dl.group_loader.create(
        name="target", description="desc", active=True, privacy=GroupPrivacyEnum.PUBLIC
    )
    # Act
    updated = await repo.update(id=target.id, obj=update_dto)

    # Assert
    assert updated.id == target.id
    assert updated.name == update_dto.name
    assert updated.description == update_dto.description
    assert updated.active == update_dto.active
    assert updated.privacy == update_dto.privacy


# pytest tests/tmain/test_group.py::test_update_name_uniq_error -v -s
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
    dl: dataloader, repo: IRepositoryGroup, create_one_dict: dict, create_two_dict: dict, update_dto: GroupUpdateDTO
):
    # Arrange
    await dl.group_loader.create(**create_one_dict)
    target_4change = await dl.group_loader.create(**create_two_dict)

    # Act & Assert
    with pytest.raises(EntityNotChange) as exc:
        await repo.update(id=target_4change.id, obj=update_dto)
    assert "Uniq failed" in str(exc.value)


# pytest tests/tmain/test_group.py::test_update_not_found_error -v -s
@pytest.mark.asyncio
async def test_update_not_found_error(dl: dataloader, repo: IRepositoryGroup):
    # Arrange
    await dl.group_loader.create()
    last_created = await dl.group_loader.create()
    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo.update(
            id=last_created.id + 1,
            obj=GroupUpdateDTO(name="changed"),
        )


async def _test_lst_user_id_param_first_variant(dl: dataloader):
    user = await dl.user_loader.create()
    user2 = await dl.user_loader.create()

    group = await dl.group_loader.create()
    group2 = await dl.group_loader.create()

    # user & user2 to group
    await dl.user_group_loader.create(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER)
    await dl.user_group_loader.create(user_id=user2.id, group_id=group.id, role=GroupRoleEnum.USER)

    # user2 to group 2
    await dl.user_group_loader.create(user_id=user2.id, group_id=group2.id, role=GroupRoleEnum.USER)

    return dict(filter_obj=GroupFilter(user_id=user.id), asrt_group_id_list=[group.id])


async def _test_lst_user_id_param_second_variant(dl: dataloader):
    user = await dl.user_loader.create()
    user2 = await dl.user_loader.create()

    group = await dl.group_loader.create()
    group2 = await dl.group_loader.create()

    # user & user2 to group
    await dl.user_group_loader.create(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER)
    await dl.user_group_loader.create(user_id=user2.id, group_id=group.id, role=GroupRoleEnum.USER)

    # user2 to group 2
    await dl.user_group_loader.create(user_id=user2.id, group_id=group2.id, role=GroupRoleEnum.USER)

    return dict(filter_obj=GroupFilter(user_id=user2.id), asrt_group_id_list=[group.id, group2.id])


async def _test_lst_user_id_param_third_variant(dl: dataloader):
    group = await dl.group_loader.create(active=True)
    group2 = await dl.group_loader.create(active=False)
    group3 = await dl.group_loader.create(active=True)

    return dict(filter_obj=GroupFilter(active=True), asrt_group_id_list=[group.id, group3.id])


# pytest tests/tmain/test_group.py::test_lst_user_id -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [
        _test_lst_user_id_param_first_variant,
        _test_lst_user_id_param_second_variant,
        _test_lst_user_id_param_third_variant,
    ],
)
async def test_lst_user_id(dl: dataloader, repo: IRepositoryGroup, arrange_func):
    # Arrange
    arrange_result: dict = await arrange_func(dl)
    filter_obj = arrange_result["filter_obj"]
    asrt_group_id_list = arrange_result["asrt_group_id_list"]

    # Act
    group_list = await repo.lst(
        filter_obj=filter_obj,
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )

    # Assert
    group_id_list = [g.id for g in group_list]
    assert set(group_id_list) == set(asrt_group_id_list)


# pytest tests/tmain/test_group.py::test_deactivate_ok -v -s
@pytest.mark.asyncio
async def test_deactivate_ok(dl: dataloader, repo: IRepositoryGroup):
    # Arrange
    group = await dl.group_loader.create(active=True)
    group2 = await dl.group_loader.create(active=True)

    # Act
    group_id = await repo.deactivate(
        id=group.id,
    )
    await dl.commit()

    # Assert
    assert group_id == group.id
    asrt_group = await repo.get(id=group.id)
    assert asrt_group.active == False
    # asrt for not changed
    asrt_group2 = await repo.get(id=group2.id)
    assert asrt_group2.active == True


# pytest tests/tmain/test_group.py::test_deactivate_not_found_error -v -s
@pytest.mark.asyncio
async def test_deactivate_not_found_error(dl: dataloader, repo: IRepositoryGroup):
    # Arrange
    await dl.group_loader.create()
    last_created = await dl.group_loader.create()

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo.deactivate(
            id=last_created.id + 1,
        )
