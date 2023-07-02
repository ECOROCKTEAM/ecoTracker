import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.community.community import CommunityCreateDTO, CommunityUpdateDTO
from src.core.dto.mock import MockObj
from src.core.entity.community import Community
from src.core.enum.community.privacy import CommunityPrivacyEnum
from src.core.exception.base import EntityNotChange, EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.community.community import CommunityFilter
from src.data.models.community.community import CommunityModel
from src.data.repository.community import IRepositoryCommunity
from tests.fixtures.community.db.entity import (
    fxe_community_default,
    fxe_community_default_2,
)
from tests.fixtures.community.db.model import (
    fxm_community_default,
    fxm_community_default_2,
)
from tests.fixtures.user.db.model import fxm_user_default
from tests.fixtures.user_community.db.model import fxm_user_community_default


# pytest tests/main/community/db/test_community.py::test_get_ok -v -s
@pytest.mark.asyncio
async def test_get_ok(repo: IRepositoryCommunity, fxe_community_default: Community):
    community = await repo.get(id=fxe_community_default.id)
    assert fxe_community_default.id == community.id
    assert fxe_community_default.name == community.name
    assert fxe_community_default.active == community.active
    assert fxe_community_default.description == community.description
    assert fxe_community_default.privacy == community.privacy


# pytest tests/main/community/db/test_community.py::test_get_not_found -v -s
@pytest.mark.asyncio
async def test_get_not_found(repo: IRepositoryCommunity):
    with pytest.raises(EntityNotFound):
        await repo.get(id=1)


# pytest tests/main/community/db/test_community.py::test_create_ok -v -s
@pytest.mark.asyncio
async def test_create_ok(session: AsyncSession, repo: IRepositoryCommunity):
    community_create = await repo.create(
        obj=CommunityCreateDTO(name="tt", privacy=CommunityPrivacyEnum.PUBLIC, description="", active=True)
    )
    await session.commit()

    community = await repo.get(id=community_create.id)
    assert community.id == community_create.id
    assert community.name == community.name
    assert community.active == community.active
    assert community.description == community.description
    assert community.privacy == community.privacy

    create_model = await session.get(entity=CommunityModel, ident={"id": community_create.id})
    assert isinstance(create_model, CommunityModel)
    await session.delete(create_model)
    await session.commit()


# pytest tests/main/community/db/test_community.py::test_create_uniq_fail -v -s
@pytest.mark.asyncio
async def test_create_uniq_fail(session: AsyncSession, repo: IRepositoryCommunity):
    community_create = await repo.create(
        obj=CommunityCreateDTO(name="tt", privacy=CommunityPrivacyEnum.PUBLIC, description="", active=True)
    )
    await session.commit()

    with pytest.raises(EntityNotCreated):
        await repo.create(
            obj=CommunityCreateDTO(name="tt", privacy=CommunityPrivacyEnum.PUBLIC, description="", active=True)
        )
        await session.commit()
    await session.rollback()

    create_model = await session.get(entity=CommunityModel, ident={"id": community_create.id})
    assert isinstance(create_model, CommunityModel)
    await session.delete(create_model)
    await session.commit()


# pytest tests/main/community/db/test_community.py::test_update_ok -v -s
@pytest.mark.asyncio
async def test_update_ok(repo: IRepositoryCommunity, fxe_community_default: Community):
    community = await repo.update(
        id=fxe_community_default.id,
        obj=CommunityUpdateDTO(
            name="changed", description="changed", active=False, privacy=CommunityPrivacyEnum.PRIVATE
        ),
    )
    assert community.id == fxe_community_default.id
    assert community.name == "changed"
    assert community.description == "changed"
    assert community.active == False
    assert community.privacy == CommunityPrivacyEnum.PRIVATE


# pytest tests/main/community/db/test_community.py::test_update_uniq_error -v -s
@pytest.mark.asyncio
async def test_update_uniq_error(
    session: AsyncSession,
    repo: IRepositoryCommunity,
    fxe_community_default: Community,
    fxe_community_default_2: Community,
):
    with pytest.raises(EntityNotChange):
        await repo.update(
            id=fxe_community_default.id,
            obj=CommunityUpdateDTO(name=fxe_community_default_2.name),
        )
    await session.rollback()


# pytest tests/main/community/db/test_community.py::test_update_not_found_error -v -s
@pytest.mark.asyncio
async def test_update_not_found_error(session: AsyncSession, repo: IRepositoryCommunity):
    with pytest.raises(EntityNotFound):
        await repo.update(
            id=1,
            obj=CommunityUpdateDTO(name="changed"),
        )
    await session.rollback()


# pytest tests/main/community/db/test_community.py::test_lst -v -s
@pytest.mark.asyncio
async def test_lst(
    repo: IRepositoryCommunity, fxe_community_default: Community, fxm_user_community_default, fxm_user_default
):
    community_list = await repo.lst(
        filter_obj=CommunityFilter(active=True, user_id=fxm_user_default.id),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    assert len(community_list) == 1
    community = community_list[0]
    assert isinstance(community, Community)
    assert community.id == fxe_community_default.id
    assert community.name == fxe_community_default.name
    assert community.description == fxe_community_default.description
    assert community.active == fxe_community_default.active
    assert community.privacy == fxe_community_default.privacy


# pytest tests/main/community/db/test_community.py::test_deactivate_ok -v -s
@pytest.mark.asyncio
async def test_deactivate_ok(session: AsyncSession, repo: IRepositoryCommunity, fxe_community_default: Community):
    community_id = await repo.deactivate(
        id=fxe_community_default.id,
    )
    await session.commit()
    assert community_id == fxe_community_default.id
    community = await repo.get(id=community_id)
    assert community.active == False


# pytest tests/main/community/db/test_community.py::test_deactivate_not_found_error -v -s
@pytest.mark.asyncio
async def test_deactivate_not_found_error(session: AsyncSession, repo: IRepositoryCommunity):
    with pytest.raises(EntityNotFound):
        await repo.deactivate(
            id=1,
        )
    await session.rollback()
