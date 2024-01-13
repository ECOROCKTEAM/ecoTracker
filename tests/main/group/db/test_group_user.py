import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.m2m.user.group import (
    UserGroupCreateDTO,
    UserGroupDTO,
    UserGroupUpdateDTO,
)
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotCreated, EntityNotDeleted, EntityNotFound
from src.core.interfaces.repository.group.group import GroupUserFilter
from src.data.models.user.user import UserGroupModel
from src.data.repository.group import IRepositoryGroup
from tests.fixtures.group.db.entity import fxe_group_default
from tests.fixtures.group.db.model import fxm_group_default
from tests.fixtures.group.db.user.entity import (
    fxe_user_group_admin,
    fxe_user_group_default,
    fxm_user_group_superuser,
)
from tests.fixtures.group.db.user.model import (
    fxm_user_group_admin,
    fxm_user_group_default,
)
from tests.fixtures.user.db.entity import fxe_user_default
from tests.fixtures.user.db.model import fxm_user_default, fxm_user_default_2
from tests.main.challenges.mission.usecases.group_mission.conftest import (
    test_user_group_admin_dto,
)


# pytest tests/main/group/db/test_group_user.py::test_get_ok -v -s
@pytest.mark.asyncio
async def test_get_ok(repo: IRepositoryGroup, fxe_user_group_default: UserGroupDTO):
    uc = await repo.user_get(group_id=fxe_user_group_default.group_id, user_id=fxe_user_group_default.user_id)
    assert fxe_user_group_default.user_id == uc.user_id
    assert fxe_user_group_default.group_id == uc.group_id
    assert fxe_user_group_default.role == uc.role


# pytest tests/main/group/db/test_group_user.py::test_get_not_found -v -s
@pytest.mark.asyncio
async def test_get_not_found(repo: IRepositoryGroup):
    with pytest.raises(EntityNotFound):
        await repo.user_get(group_id=1, user_id="1")


# pytest tests/main/group/db/test_group_user.py::test_add_ok -v -s
@pytest.mark.asyncio
async def test_add_ok(
    session: AsyncSession,
    repo: IRepositoryGroup,
    fxe_user_default: User,
    fxe_group_default: Group,
):
    uc = await repo.user_add(
        obj=UserGroupCreateDTO(group_id=fxe_group_default.id, user_id=fxe_user_default.id, role=GroupRoleEnum.ADMIN)
    )
    await session.commit()
    assert fxe_user_default.id == uc.user_id
    assert fxe_group_default.id == uc.group_id
    assert GroupRoleEnum.ADMIN == uc.role

    create_model = await session.get(entity=UserGroupModel, ident={"user_id": uc.user_id, "group_id": uc.group_id})
    assert isinstance(create_model, UserGroupModel)
    await session.delete(create_model)
    await session.commit()


# pytest tests/main/group/db/test_group_user.py::test_add_fail_fk -v -s
@pytest.mark.asyncio
async def test_add_fail_fk(
    session: AsyncSession,
    repo: IRepositoryGroup,
    fxe_user_default: User,
    fxe_group_default: Group,
):
    with pytest.raises(EntityNotCreated):
        await repo.user_add(
            obj=UserGroupCreateDTO(group_id=66666, user_id=fxe_user_default.id, role=GroupRoleEnum.ADMIN)
        )
    await session.rollback()

    with pytest.raises(EntityNotCreated):
        await repo.user_add(
            obj=UserGroupCreateDTO(group_id=fxe_group_default.id, user_id="66666", role=GroupRoleEnum.ADMIN)
        )
    await session.rollback()


# pytest tests/main/group/db/test_group_user.py::test_add_fail_uniq -v -s
@pytest.mark.asyncio
async def test_add_fail_uniq(session: AsyncSession, repo: IRepositoryGroup, fxe_user_group_default: UserGroupDTO):
    with pytest.raises(EntityNotCreated):
        await repo.user_add(
            obj=UserGroupCreateDTO(
                group_id=fxe_user_group_default.group_id,
                user_id=fxe_user_group_default.user_id,
                role=GroupRoleEnum.ADMIN,
            )
        )
    await session.rollback()


# pytest tests/main/group/db/test_group_user.py::test_lst -v -s
@pytest.mark.asyncio
async def test_lst(
    repo: IRepositoryGroup,
    fxm_user_group_superuser: UserGroupDTO,
    fxm_user_group_admin: UserGroupDTO,
):
    uc_list = await repo.user_list(
        id=fxm_user_group_admin.group_id,
        filter_obj=GroupUserFilter(role__in=[fxm_user_group_admin.role], user_id__in=[fxm_user_group_admin.user_id]),
    )
    assert len(uc_list) == 1
    uc = uc_list[0]
    assert fxm_user_group_admin.user_id == uc.user_id
    assert fxm_user_group_admin.group_id == uc.group_id
    assert fxm_user_group_admin.role == uc.role

    uc_list = await repo.user_list(
        id=fxm_user_group_admin.group_id,
        filter_obj=GroupUserFilter(
            role__in=[fxm_user_group_superuser.role], user_id__in=[fxm_user_group_superuser.user_id]
        ),
    )
    assert len(uc_list) == 1
    uc = uc_list[0]
    assert fxm_user_group_superuser.user_id == uc.user_id
    assert fxm_user_group_superuser.group_id == uc.group_id
    assert fxm_user_group_superuser.role == uc.role

    uc_list = await repo.user_list(
        id=fxm_user_group_admin.group_id,
        filter_obj=GroupUserFilter(user_id__in=[fxm_user_group_superuser.user_id, fxm_user_group_admin.user_id]),
    )
    assert len(uc_list) == 2
    user_ids = [x.user_id for x in uc_list]
    assert fxm_user_group_admin.user_id in user_ids
    assert fxm_user_group_superuser.user_id in user_ids


# pytest tests/main/group/db/test_group_user.py::test_role_update_ok -v -s
@pytest.mark.asyncio
async def test_role_update_ok(repo: IRepositoryGroup, fxe_user_group_default: UserGroupDTO):
    uc = await repo.user_role_update(
        group_id=fxe_user_group_default.group_id,
        user_id=fxe_user_group_default.user_id,
        obj=UserGroupUpdateDTO(role=GroupRoleEnum.BLOCKED),
    )
    assert fxe_user_group_default.user_id == uc.user_id
    assert fxe_user_group_default.group_id == uc.group_id
    assert GroupRoleEnum.BLOCKED == uc.role


# pytest tests/main/group/db/test_group_user.py::test_role_update_not_found -v -s
@pytest.mark.asyncio
async def test_role_update_not_found(
    repo: IRepositoryGroup,
):
    with pytest.raises(EntityNotFound):
        await repo.user_role_update(group_id=1, user_id="1", obj=UserGroupUpdateDTO(role=GroupRoleEnum.BLOCKED))


# pytest tests/main/group/db/test_group_user.py::test_user_remove_ok -v -s
@pytest.mark.asyncio
async def test_user_remove_ok(
    session: AsyncSession,
    repo: IRepositoryGroup,
    fxe_user_default: User,
    fxe_group_default: Group,
):
    uc = await repo.user_add(
        obj=UserGroupCreateDTO(group_id=fxe_group_default.id, user_id=fxe_user_default.id, role=GroupRoleEnum.ADMIN)
    )
    await session.commit()
    assert fxe_user_default.id == uc.user_id
    assert fxe_group_default.id == uc.group_id
    assert GroupRoleEnum.ADMIN == uc.role

    status = await repo.user_remove(group_id=uc.group_id, user_id=uc.user_id)
    await session.commit()
    assert status is True


# pytest tests/main/group/db/test_group_user.py::test_user_remove_false -v -s
@pytest.mark.asyncio
async def test_user_remove_false(
    session: AsyncSession,
    repo: IRepositoryGroup,
):
    with pytest.raises(EntityNotDeleted):
        await repo.user_remove(group_id=6666, user_id="6666")
    await session.commit()
