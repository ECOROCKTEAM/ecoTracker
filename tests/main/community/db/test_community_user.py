import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.m2m.user.community import (
    UserCommunityCreateDTO,
    UserCommunityDTO,
    UserCommunityUpdateDTO,
)
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.community.community import CommunityUserFilter
from src.data.models.user.user import UserCommunityModel
from src.data.repository.community import IRepositoryCommunity
from tests.fixtures.community.db.entity import fxe_community_default
from tests.fixtures.community.db.model import fxm_community_default
from tests.fixtures.community.db.user.entity import (
    fxe_user_community_admin,
    fxe_user_community_default,
    fxm_user_community_superuser,
)
from tests.fixtures.community.db.user.model import (
    fxm_user_community_admin,
    fxm_user_community_default,
)
from tests.fixtures.user.db.entity import fxe_user_default
from tests.fixtures.user.db.model import fxm_user_default, fxm_user_default_2
from tests.main.challenges.mission.usecases.community_mission.conftest import (
    test_user_community_admin_dto,
)


# pytest tests/main/community/db/test_community_user.py::test_get_ok -v -s
@pytest.mark.asyncio
async def test_get_ok(repo: IRepositoryCommunity, fxe_user_community_default: UserCommunityDTO):
    uc = await repo.user_get(
        community_id=fxe_user_community_default.community_id, user_id=fxe_user_community_default.user_id
    )
    assert fxe_user_community_default.user_id == uc.user_id
    assert fxe_user_community_default.community_id == uc.community_id
    assert fxe_user_community_default.role == uc.role


# pytest tests/main/community/db/test_community_user.py::test_get_not_found -v -s
@pytest.mark.asyncio
async def test_get_not_found(repo: IRepositoryCommunity):
    with pytest.raises(EntityNotFound):
        await repo.user_get(community_id=1, user_id=1)


# pytest tests/main/community/db/test_community_user.py::test_add_ok -v -s
@pytest.mark.asyncio
async def test_add_ok(
    session: AsyncSession,
    repo: IRepositoryCommunity,
    fxe_user_default: User,
    fxe_community_default: Community,
):
    uc = await repo.user_add(
        obj=UserCommunityCreateDTO(
            community_id=fxe_community_default.id, user_id=fxe_user_default.id, role=CommunityRoleEnum.ADMIN
        )
    )
    await session.commit()
    assert fxe_user_default.id == uc.user_id
    assert fxe_community_default.id == uc.community_id
    assert CommunityRoleEnum.ADMIN == uc.role

    create_model = await session.get(
        entity=UserCommunityModel, ident={"user_id": uc.user_id, "community_id": uc.community_id}
    )
    assert isinstance(create_model, UserCommunityModel)
    await session.delete(create_model)
    await session.commit()


# pytest tests/main/community/db/test_community_user.py::test_add_fail_fk -v -s
@pytest.mark.asyncio
async def test_add_fail_fk(
    session: AsyncSession,
    repo: IRepositoryCommunity,
    fxe_user_default: User,
    fxe_community_default: Community,
):
    with pytest.raises(EntityNotCreated):
        await repo.user_add(
            obj=UserCommunityCreateDTO(community_id=66666, user_id=fxe_user_default.id, role=CommunityRoleEnum.ADMIN)
        )
    await session.rollback()

    with pytest.raises(EntityNotCreated):
        await repo.user_add(
            obj=UserCommunityCreateDTO(
                community_id=fxe_community_default.id, user_id=66666, role=CommunityRoleEnum.ADMIN
            )
        )
    await session.rollback()


# pytest tests/main/community/db/test_community_user.py::test_add_fail_uniq -v -s
@pytest.mark.asyncio
async def test_add_fail_uniq(
    session: AsyncSession, repo: IRepositoryCommunity, fxe_user_community_default: UserCommunityDTO
):
    with pytest.raises(EntityNotCreated):
        await repo.user_add(
            obj=UserCommunityCreateDTO(
                community_id=fxe_user_community_default.community_id,
                user_id=fxe_user_community_default.user_id,
                role=CommunityRoleEnum.ADMIN,
            )
        )
    await session.rollback()


# pytest tests/main/community/db/test_community_user.py::test_lst -v -s
@pytest.mark.asyncio
async def test_lst(
    repo: IRepositoryCommunity,
    fxm_user_community_superuser: UserCommunityDTO,
    fxm_user_community_admin: UserCommunityDTO,
):
    uc_list = await repo.user_list(
        id=fxm_user_community_admin.community_id,
        filter_obj=CommunityUserFilter(
            role_list=[fxm_user_community_admin.role], user_id__in=[fxm_user_community_admin.user_id]
        ),
    )
    assert len(uc_list) == 1
    uc = uc_list[0]
    assert fxm_user_community_admin.user_id == uc.user_id
    assert fxm_user_community_admin.community_id == uc.community_id
    assert fxm_user_community_admin.role == uc.role

    uc_list = await repo.user_list(
        id=fxm_user_community_admin.community_id,
        filter_obj=CommunityUserFilter(
            role_list=[fxm_user_community_superuser.role], user_id__in=[fxm_user_community_superuser.user_id]
        ),
    )
    assert len(uc_list) == 1
    uc = uc_list[0]
    assert fxm_user_community_superuser.user_id == uc.user_id
    assert fxm_user_community_superuser.community_id == uc.community_id
    assert fxm_user_community_superuser.role == uc.role

    uc_list = await repo.user_list(
        id=fxm_user_community_admin.community_id,
        filter_obj=CommunityUserFilter(
            user_id__in=[fxm_user_community_superuser.user_id, fxm_user_community_admin.user_id]
        ),
    )
    assert len(uc_list) == 2
    user_ids = [x.user_id for x in uc_list]
    assert fxm_user_community_admin.user_id in user_ids
    assert fxm_user_community_superuser.user_id in user_ids


# pytest tests/main/community/db/test_community_user.py::test_role_update_ok -v -s
@pytest.mark.asyncio
async def test_role_update_ok(repo: IRepositoryCommunity, fxe_user_community_default: UserCommunityDTO):
    uc = await repo.user_role_update(
        community_id=fxe_user_community_default.community_id,
        user_id=fxe_user_community_default.user_id,
        obj=UserCommunityUpdateDTO(role=CommunityRoleEnum.BLOCKED),
    )
    assert fxe_user_community_default.user_id == uc.user_id
    assert fxe_user_community_default.community_id == uc.community_id
    assert CommunityRoleEnum.BLOCKED == uc.role


# pytest tests/main/community/db/test_community_user.py::test_role_update_not_found -v -s
@pytest.mark.asyncio
async def test_role_update_not_found(
    repo: IRepositoryCommunity,
):
    with pytest.raises(EntityNotFound):
        await repo.user_role_update(
            community_id=1, user_id=1, obj=UserCommunityUpdateDTO(role=CommunityRoleEnum.BLOCKED)
        )


# pytest tests/main/community/db/test_community_user.py::test_user_remove_ok -v -s
@pytest.mark.asyncio
async def test_user_remove_ok(
    session: AsyncSession,
    repo: IRepositoryCommunity,
    fxe_user_default: User,
    fxe_community_default: Community,
):
    uc = await repo.user_add(
        obj=UserCommunityCreateDTO(
            community_id=fxe_community_default.id, user_id=fxe_user_default.id, role=CommunityRoleEnum.ADMIN
        )
    )
    await session.commit()
    assert fxe_user_default.id == uc.user_id
    assert fxe_community_default.id == uc.community_id
    assert CommunityRoleEnum.ADMIN == uc.role

    status = await repo.user_remove(community_id=uc.community_id, user_id=uc.user_id)
    await session.commit()
    assert status is True


# pytest tests/main/community/db/test_community_user.py::test_user_remove_false -v -s
@pytest.mark.asyncio
async def test_user_remove_false(
    session: AsyncSession,
    repo: IRepositoryCommunity,
):
    status = await repo.user_remove(community_id=6666, user_id=6666)
    await session.commit()
    assert status is False
