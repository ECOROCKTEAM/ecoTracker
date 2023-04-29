import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, text
from src.application.database.base import Base
from src.data.models import *
from tests.fixtures import *  # fixtures must be imported

from src.data.models.user.user import UserModel, UserTaskModel
from src.data.models.task.task import TaskModel
from src.data.models.shared.occupancy import OccupancyStatusModel, OccupancyTypeModel
from src.data.models.translate.task import TaskTranslateModel
from src.data.models.translate.occupancy import OccupancyStatusTranslateModel, OccupancyTypeTranslateModel



@pytest.mark.asyncio
async def test_example(session: AsyncSession):
    stmt = select(UserModel)
    user = await session.scalar(stmt)
    print(user)
    stmt = select(TaskModel).join(
        UserTaskModel, and_(UserTaskModel.username == user.username, TaskModel.id == UserTaskModel.id) # type: ignore
    )
    task = await session.scalar(stmt)
    stmt = select(OccupancyTypeModel).where(OccupancyTypeModel.id == TaskModel.occupancy_id)
    occupancy_type = await session.scalar(stmt)
    print(task, occupancy_type)
    stmt = select(TaskTranslateModel).where(TaskTranslateModel.task_id == task.id) # type: ignore
    task_translated = await session.scalars(stmt)
    for tt in task_translated:
        print("\t", tt)
