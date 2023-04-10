from typing import List
import pytest
from sqlalchemy import text
from src.application.database.holder import Database, Base
from src.application.settings import get_settings

from src.data.models import *

s = get_settings()
db = Database(database_url=s.DATABASE_URL, echo=False)
db.setup()

@pytest.mark.asyncio
async def test_creation():
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print()
    async with db.session() as session:
        r = await session.execute(text("select 1"))
        print(r.all())


