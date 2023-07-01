import pytest
from sqlalchemy import and_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.database.base import Base
from src.data.models import *


# pytest tests/test_common.py::test_database_connect -v -s
@pytest.mark.asyncio
async def test_database_connect(session: AsyncSession):
    stmt = text("select 1")
    r = await session.execute(stmt)
    result = r.one_or_none()
    assert result is not None
