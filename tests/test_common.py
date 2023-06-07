import pytest
from sqlalchemy import and_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.database.base import Base
from src.data.models import *


@pytest.mark.asyncio
async def test_database_connect(session: AsyncSession):
    stmt = text("select 1")
    r = await session.execute(stmt)
    print(r.fetchall())
