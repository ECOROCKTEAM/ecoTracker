import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.group.group import GroupCreateDTO, GroupUpdateDTO
from src.core.dto.mock import MockObj
from src.core.entity.group import Group
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.exception.base import EntityNotChange, EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.group.group import GroupFilter
from src.data.models.group.group import GroupModel
from src.data.repository.group import IRepositoryGroup
from tests.fixtures.group.db.entity import fxe_group_default, fxe_group_default_2
from tests.fixtures.group.db.model import fxm_group_default, fxm_group_default_2
from tests.fixtures.group.db.user.model import fxm_user_group_default
from tests.fixtures.user.db.model import fxm_user_default


# pytest tests/main/group/db/test_group.py::test_get_ok -v -s
@pytest.mark.asyncio
async def test_get_ok(repo: IRepositoryGroup, fxe_group_default: Group):
    group = await repo.get(id=fxe_group_default.id)
    assert fxe_group_default.id == group.id
    assert fxe_group_default.name == group.name
    assert fxe_group_default.active == group.active
    assert fxe_group_default.description == group.description
    assert fxe_group_default.privacy == group.privacy


# pytest tests/main/group/db/test_group.py::test_get_not_found -v -s
@pytest.mark.asyncio
async def test_get_not_found(repo: IRepositoryGroup):
    with pytest.raises(EntityNotFound):
        await repo.get(id=1)


# pytest tests/main/group/db/test_group.py::test_create_ok -v -s
@pytest.mark.asyncio
async def test_create_ok(session: AsyncSession, repo: IRepositoryGroup):
    group_create = await repo.create(
        obj=GroupCreateDTO(name="tt", privacy=GroupPrivacyEnum.PUBLIC, description="", active=True)
    )
    await session.commit()

    group = await repo.get(id=group_create.id)
    assert group.id == group_create.id
    assert group.name == group.name
    assert group.active == group.active
    assert group.description == group.description
    assert group.privacy == group.privacy

    create_model = await session.get(entity=GroupModel, ident={"id": group_create.id})
    assert isinstance(create_model, GroupModel)
    await session.delete(create_model)
    await session.commit()


# pytest tests/main/group/db/test_group.py::test_create_uniq_fail -v -s
@pytest.mark.asyncio
async def test_create_uniq_fail(session: AsyncSession, repo: IRepositoryGroup):
    group_create = await repo.create(
        obj=GroupCreateDTO(name="tt", privacy=GroupPrivacyEnum.PUBLIC, description="", active=True)
    )
    await session.commit()

    with pytest.raises(EntityNotCreated):
        await repo.create(obj=GroupCreateDTO(name="tt", privacy=GroupPrivacyEnum.PUBLIC, description="", active=True))
        await session.commit()
    await session.rollback()

    create_model = await session.get(entity=GroupModel, ident={"id": group_create.id})
    assert isinstance(create_model, GroupModel)
    await session.delete(create_model)
    await session.commit()


# pytest tests/main/group/db/test_group.py::test_update_ok -v -s
@pytest.mark.asyncio
async def test_update_ok(repo: IRepositoryGroup, fxe_group_default: Group):
    group = await repo.update(
        id=fxe_group_default.id,
        obj=GroupUpdateDTO(name="changed", description="changed", active=False, privacy=GroupPrivacyEnum.PRIVATE),
    )
    assert group.id == fxe_group_default.id
    assert group.name == "changed"
    assert group.description == "changed"
    assert group.active == False
    assert group.privacy == GroupPrivacyEnum.PRIVATE


# pytest tests/main/group/db/test_group.py::test_update_uniq_error -v -s
@pytest.mark.asyncio
async def test_update_uniq_error(
    session: AsyncSession,
    repo: IRepositoryGroup,
    fxe_group_default: Group,
    fxe_group_default_2: Group,
):
    with pytest.raises(EntityNotChange):
        await repo.update(
            id=fxe_group_default.id,
            obj=GroupUpdateDTO(name=fxe_group_default_2.name),
        )
    await session.rollback()


# pytest tests/main/group/db/test_group.py::test_update_not_found_error -v -s
@pytest.mark.asyncio
async def test_update_not_found_error(session: AsyncSession, repo: IRepositoryGroup):
    with pytest.raises(EntityNotFound):
        await repo.update(
            id=1,
            obj=GroupUpdateDTO(name="changed"),
        )
    await session.rollback()


# pytest tests/main/group/db/test_group.py::test_lst -v -s
@pytest.mark.asyncio
async def test_lst(repo: IRepositoryGroup, fxe_group_default: Group, fxm_user_group_default, fxm_user_default):
    group_list = await repo.lst(
        filter_obj=GroupFilter(active=True, user_id=fxm_user_default.id),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    assert len(group_list) == 1
    group = group_list[0]
    assert isinstance(group, Group)
    assert group.id == fxe_group_default.id
    assert group.name == fxe_group_default.name
    assert group.description == fxe_group_default.description
    assert group.active == fxe_group_default.active
    assert group.privacy == fxe_group_default.privacy


# pytest tests/main/group/db/test_group.py::test_deactivate_ok -v -s
@pytest.mark.asyncio
async def test_deactivate_ok(session: AsyncSession, repo: IRepositoryGroup, fxe_group_default: Group):
    group_id = await repo.deactivate(
        id=fxe_group_default.id,
    )
    await session.commit()
    assert group_id == fxe_group_default.id
    group = await repo.get(id=group_id)
    assert group.active == False


# pytest tests/main/Group/db/test_Group.py::test_deactivate_not_found_error -v -s
@pytest.mark.asyncio
async def test_deactivate_not_found_error(session: AsyncSession, repo: IRepositoryGroup):
    with pytest.raises(EntityNotFound):
        await repo.deactivate(
            id=1,
        )
    await session.rollback()
