import pytest
from sqlalchemy import and_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.database.base import Base
from src.data.models import *


# python -m pytest tests/test_common.py::test_database_connect -v -s
@pytest.mark.asyncio
async def test_database_connect(session: AsyncSession):
    # stmt = text("select 1")
    # r = await session.execute(stmt)
    # result = r.one_or_none()
    # assert result is not None
    user = UserModel(username="as", password="a", active=True, language=LanguageEnum.RU)
    session.add(user)
    await session.flush()

    category = OccupancyCategoryModel()
    session.add(category)
    await session.flush()

    # task
    task = TaskModel(score=111, active=True, category_id=category.id)
    session.add(task)
    await session.flush()
    user_task = UserTaskModel(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.ACTIVE)
    session.add(user_task)
    await session.commit()
    await session.refresh(user_task)
    print()
    print("#task")
    print("created")
    print(user_task.date_start, user_task.date_close)

    user_task.status = OccupancyStatusEnum.FINISH
    user_task.date_close = datetime.now()
    session.add(user_task)
    await session.commit()
    await session.refresh(user_task)
    print("update")
    print(user_task.date_start, user_task.date_close)

    # mission
    mission = MissionModel(score=111, active=True, author="d", category_id=category.id)
    session.add(mission)
    await session.flush()

    user_mission = UserMissionModel(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)
    session.add(user_mission)
    await session.commit()
    await session.refresh(user_mission)
    print()
    print("#mission")
    print("created")
    print(user_mission.date_start, user_mission.date_close)

    user_mission.status = OccupancyStatusEnum.FINISH
    user_mission.date_close = datetime.now()
    session.add(user_mission)
    await session.commit()
    await session.refresh(user_mission)
    print("update")
    print(user_mission.date_start, user_mission.date_close)
