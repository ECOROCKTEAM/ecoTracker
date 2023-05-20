from dataclasses import asdict

import pytest

from src.core.dto.community.community import CommunityCreateDTO, CommunityUpdateDTO
from src.core.entity.community import Community, CommunityPrivacyEnum
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
