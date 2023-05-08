import pytest
from dataclasses import asdict
from src.data.repository.community import RepositoryCommunity

from src.core.entity.community import Community, CommunityPrivacyEnum
from src.data.unit_of_work import SqlAlchemyUnitOfWork
from src.core.dto.community.community import CommunityUpdateDTO, CommunityCreateDTO

# python -m pytest tests/db/test_community.py


@pytest.mark.asyncio
async def test_get(pool):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        res = await uow.community.get(id="asd")
    print(res)
    assert res is None


@pytest.mark.asyncio
async def test_create(pool):
    dto = CommunityCreateDTO(name="test-comm-1", privacy=CommunityPrivacyEnum.PRIVATE)
    async with SqlAlchemyUnitOfWork(pool) as uow:
        res = await uow.community.create(obj=dto)
        await uow.commit()

    assert res == Community(**asdict(dto), id=res.id)
