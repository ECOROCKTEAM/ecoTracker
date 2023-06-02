from dataclasses import asdict

import pytest

from src.core.dto.community.community import CommunityCreateDTO, CommunityUpdateDTO
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.dto.mock import MockObj
from src.core.entity.community import Community, CommunityPrivacyEnum
from src.core.entity.user import User
from src.core.interfaces.repository.community.community import CommunityFilter
from src.data.repository.community import RepositoryCommunity
from src.data.unit_of_work import SqlAlchemyUnitOfWork

# python -m pytest tests/db/test_community.py


@pytest.mark.asyncio
async def test_get(pool):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        with pytest.raises(Exception):
            res = await uow.community.get(id=1)


@pytest.mark.asyncio
async def test_create(pool):
    dto = CommunityCreateDTO(name="test-comm-1", privacy=CommunityPrivacyEnum.PRIVATE)
    async with SqlAlchemyUnitOfWork(pool) as uow:
        res = await uow.community.create(obj=dto)
        await uow.commit()

    assert res == Community(**asdict(dto), id=res.id)


# python -m pytest tests/db/test_community.py::test_lst -v -s
@pytest.mark.asyncio
async def test_lst(pool, test_user: User, test_user_community: UserCommunityDTO):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        community_list = await uow.community.lst(
            filter_obj=CommunityFilter(), order_obj=MockObj(), pagination_obj=MockObj()
        )
        await uow.commit()
    assert len(community_list) != 0
    assert test_user_community.community_id in [c.id for c in community_list]
