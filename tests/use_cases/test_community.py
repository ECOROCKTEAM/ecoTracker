from dataclasses import asdict

import pytest

from src.core.dto.community.community import CommunityCreateDTO, CommunityUpdateDTO
from src.core.dto.community.invite import CommunityInviteDTO
from src.core.dto.m2m.user.community import UserCommunityUpdateDTO
from src.core.dto.mock import MockObj
from src.core.entity.user import User
from src.core.enum.community.privacy import CommunityPrivacyEnum
from src.core.enum.community.role import CommunityRoleEnum
from src.core.interfaces.repository.community.community import CommunityFilter
from src.core.usecases.community import (
    community_change_user_role,
    community_create,
    community_delete,
    community_get_invite_link,
    community_join_by_code,
    community_leave,
    community_list,
    community_public_add_user,
    community_update,
)
from src.data.unit_of_work import SqlAlchemyUnitOfWork

DAY_SECONDS = 86000


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
async def test_delete(pool, test_user, test_community_delete):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = community_delete.CommunityDeleteUsecase(uow=uow)
    res = await uc(user=test_user, community_id=test_community_delete.id)
    assert res.item == test_community_delete.id


@pytest.mark.asyncio
async def test_get_invite(pool, test_user, test_community):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = community_get_invite_link.CommunityGetInviteLinkUsecase(uow=uow, invite_expire_sec=DAY_SECONDS)
    res = await uc(community_id=test_community.id, user=test_user)
    assert isinstance(res.item, CommunityInviteDTO)
    assert len(res.item.code) == 32


@pytest.mark.asyncio
async def test_leave(pool, test_user_leave, test_community, test_user_community_leave):
    # test_user_community_leave for create test user role(m2m)
    uow = SqlAlchemyUnitOfWork(pool)
    uc = community_leave.CommunityLeaveUsecase(uow=uow)
    res = await uc(user=test_user_leave, community_id=test_community.id)
    assert isinstance(res.item, bool)
    assert res.item


@pytest.mark.asyncio
async def test_join_by_code(pool, test_user_join_by_code, test_community_join_code):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = community_join_by_code.CommunityJoinByCode(uow=uow)
    res = await uc(user=test_user_join_by_code, code=test_community_join_code.code)
    assert res.item.role == CommunityRoleEnum.USER


@pytest.mark.asyncio
async def test_public_add(pool, test_user_join, test_community):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = community_public_add_user.CommunityPublicAddUserUsecase(uow=uow)
    res = await uc(user=test_user_join, community_id=test_community.id)
    assert res.item.role == CommunityRoleEnum.USER
