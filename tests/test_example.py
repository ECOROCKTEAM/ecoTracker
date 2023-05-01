import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, text
from src.application.database.base import Base
from src.data.models import *


@pytest.mark.asyncio
async def test_example(session: AsyncSession):
    stmt = text("select 1")
    r = await session.execute(stmt)
    print(r.fetchall())
    # stmt = select(UserModel)
    # user = await session.scalar(stmt)
    # print(user)
    # stmt = select(TaskModel).join(
    #     UserTaskModel, and_(UserTaskModel.username == user.username, TaskModel.id == UserTaskModel.id)  # type: ignore
    # )
    # task = await session.scalar(stmt)
    # stmt = select(OccupancyCategoryModel).where(OccupancyCategoryModel.id == TaskModel.occupancy_id)
    # occupancy_type = await session.scalar(stmt)
    # print(task, occupancy_type)
    # stmt = select(TaskTranslateModel).where(TaskTranslateModel.task_id == task.id)  # type: ignore
    # task_translated = await session.scalars(stmt)
    # for tt in task_translated:
    #     print("\t", tt)
