import pytest
from dataclasses import asdict

from src.core.entity.user import User
from src.core.dto.mock import MockObj
from src.core.dto.community.community import CommunityCreateDTO, CommunityUpdateDTO
from src.core.dto.m2m.user.community import UserCommunityUpdateDTO
from src.core.enum.community.privacy import CommunityPrivacyEnum
from src.core.enum.community.role import CommunityRoleEnum
from src.core.interfaces.repository.community.community import CommunityFilter
from src.data.unit_of_work import SqlAlchemyUnitOfWork
from src.core.usecases.community import (
    community_delete,
    community_list,
    community_create,
    community_update,
    community_change_user_role,
    community_get_invite_link,
    community_public_add_user,
)


@pytest.mark.asyncio
async def test_create(pool, test_user):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = community_create.CommunityCreateUsecase(uow=uow)

    res = await uc(
        create_obj=CommunityCreateDTO(name="test-com1", privacy=CommunityPrivacyEnum.PRIVATE), user=test_user
    )
    assert res.item.id is not None


@pytest.mark.asyncio
async def test_update(pool, test_user, test_community, test_user_community):
    uow = SqlAlchemyUnitOfWork(pool)
    update_obj = CommunityUpdateDTO(
        name="new_name", description="new_description", privacy=CommunityPrivacyEnum.PUBLICK
    )
    uc = community_update.CommunityUpdateUsecase(uow=uow)
    res = await uc(community_id=test_community.id, user=test_user, update_obj=update_obj)
    assert res.item.id == test_community.id
    assert res.item.active == test_community.active

    assert res.item.name == update_obj.name
    assert res.item.description == update_obj.description
    assert res.item.privacy == update_obj.privacy


@pytest.mark.asyncio
async def test_list(pool, test_user, test_community):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = community_list.CommunityListUsecase(uow=uow)
    res = await uc(user=test_user, filter_obj=CommunityFilter(), order_obj=MockObj(), pagination_obj=MockObj())
    assert isinstance(res.item, list)
    assert test_community.id in [comm.id for comm in res.item]


@pytest.mark.asyncio
async def test_change_role(pool, test_user, test_community, test_user_role, test_user_community_change):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = community_change_user_role.CommunityChangeUserRoleUsecase(uow=uow)
    res = await uc(
        user=test_user,
        user_id=test_user_role.id,
        community_id=test_community.id,
        update_obj=UserCommunityUpdateDTO(role=CommunityRoleEnum.ADMIN),
    )
    assert res.item.role == CommunityRoleEnum.ADMIN
    assert res.item.user_id == test_user_role.id
    assert res.item.community_id == test_community.id


@pytest.mark.asyncio
async def test_list(pool, test_user, test_community_delete):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = community_delete.CommunityDeleteUsecase(uow=uow)
    res = await uc(user=test_user, community_id=test_community_delete.id)
    assert res.item == test_community_delete.id
