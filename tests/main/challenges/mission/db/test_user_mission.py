from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.mission import MissionUserCreateDTO, MissionUserUpdateDTO
from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission, MissionUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.challenges.mission import MissionUserFilter
from src.data.models.challenges.mission import UserMissionModel
from src.data.models.user.user import UserModel
from src.data.repository.challenges.mission import RepositoryMission
from tests.fixtures.challenges.category.db.model import fxm_category_default
from tests.fixtures.challenges.mission.db.entity import fxe_mission_default
from tests.fixtures.challenges.mission.db.model import fxm_mission_default
from tests.fixtures.challenges.mission.db.user.entity import fxe_user_mission_default
from tests.fixtures.challenges.mission.db.user.model import fxm_user_mission_default
from tests.fixtures.user.db.entity import fxe_user_default
from tests.fixtures.user.db.model import fxm_user_default


# pytest tests/main/challenges/mission/db/test_user_mission.py::test_get_user_mission_ok -v -s
@pytest.mark.asyncio
async def test_get_user_mission_ok(repo: RepositoryMission, fxe_user_mission_default: MissionUser):
    mission = await repo.user_mission_get(id=fxe_user_mission_default.id, user_id=fxe_user_mission_default.user_id)
    assert fxe_user_mission_default.id == mission.id
    assert fxe_user_mission_default.user_id == mission.user_id
    assert fxe_user_mission_default.mission_id == mission.mission_id
    assert fxe_user_mission_default.date_start == mission.date_start
    assert fxe_user_mission_default.date_close == mission.date_close
    assert fxe_user_mission_default.status == mission.status


# pytest tests/main/challenges/mission/db/test_user_mission.py::test_get_user_mission_not_found -v -s
@pytest.mark.asyncio
async def test_get_user_mission_not_found(repo: RepositoryMission):
    with pytest.raises(EntityNotFound):
        _ = await repo.user_mission_get(id=-1, user_id="1")


# pytest tests/main/challenges/mission/db/test_user_mission.py::test_create_user_mission_ok -v -s
@pytest.mark.asyncio
async def test_create_user_mission_ok(
    session: AsyncSession, repo: RepositoryMission, fxe_user_default: User, fxe_mission_default: Mission
):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    user_mission_list = await repo.user_mission_lst(
        user_id=fxe_user_default.id, filter_obj=MissionUserFilter(), **default_kw
    )
    assert len(user_mission_list) == 0
    user_mission = await repo.user_mission_create(
        user_id=fxe_user_default.id,
        obj=MissionUserCreateDTO(
            mission_id=fxe_mission_default.id,
        ),
    )
    await session.commit()
    assert user_mission.id is not None
    assert user_mission.user_id == fxe_user_default.id
    assert user_mission.mission_id == fxe_mission_default.id
    assert isinstance(user_mission.date_start, datetime)
    assert user_mission.date_close is None
    assert user_mission.status == OccupancyStatusEnum.ACTIVE

    user_mission_list = await repo.user_mission_lst(
        user_id=fxe_user_default.id, filter_obj=MissionUserFilter(), **default_kw
    )
    assert len(user_mission_list) == 1

    create_model = await session.get(entity=UserMissionModel, ident={"id": user_mission.id})
    assert isinstance(create_model, UserMissionModel)
    await session.delete(create_model)
    await session.commit()


# pytest tests/main/challenges/mission/db/test_user_mission.py::test_create_user_mission_not_created -v -s
@pytest.mark.asyncio
async def test_create_user_mission_not_created(
    session: AsyncSession, repo: RepositoryMission, fxe_user_default: User, fxe_mission_default: Mission
):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    user_mission_list = await repo.user_mission_lst(
        user_id=fxe_user_default.id, filter_obj=MissionUserFilter(), **default_kw
    )
    assert len(user_mission_list) == 0
    with pytest.raises(EntityNotCreated):
        _ = await repo.user_mission_create(
            user_id="-1",
            obj=MissionUserCreateDTO(
                mission_id=fxe_mission_default.id,
            ),
        )
    await session.rollback()
    user_mission_list = await repo.user_mission_lst(
        user_id=fxe_user_default.id, filter_obj=MissionUserFilter(), **default_kw
    )
    assert len(user_mission_list) == 0


# pytest tests/main/challenges/mission/db/test_user_mission.py::test_update_user_mission -v -s
@pytest.mark.asyncio
async def test_update_user_mission(
    session: AsyncSession,
    repo: RepositoryMission,
    fxe_user_mission_default: MissionUser,
):
    assert fxe_user_mission_default.status == OccupancyStatusEnum.ACTIVE
    assert fxe_user_mission_default.date_close is None

    updated = await repo.user_mission_update(
        id=fxe_user_mission_default.id,
        user_id=fxe_user_mission_default.user_id,
        obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.FINISH),
    )
    await session.commit()

    assert isinstance(updated.date_close, datetime)
    assert updated.status == OccupancyStatusEnum.FINISH

    date_after_update = updated.date_close

    updated_second = await repo.user_mission_update(
        id=fxe_user_mission_default.id,
        user_id=fxe_user_mission_default.user_id,
        obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.REJECT),
    )
    await session.commit()

    assert isinstance(updated_second.date_close, datetime)
    assert updated_second.status == OccupancyStatusEnum.REJECT
    assert updated_second.date_close > date_after_update


# pytest tests/main/challenges/mission/db/test_user_mission.py::test_update_user_mission_not_found -v -s
@pytest.mark.asyncio
async def test_update_user_mission_not_found(
    repo: RepositoryMission,
    fxe_user_mission_default: MissionUser,
):
    with pytest.raises(EntityNotFound):
        _ = await repo.user_mission_update(
            id=-1, user_id=fxe_user_mission_default.user_id, obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.FINISH)
        )
    with pytest.raises(EntityNotFound):
        _ = await repo.user_mission_update(
            id=fxe_user_mission_default.id, user_id="-1", obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.FINISH)
        )

    with pytest.raises(EntityNotFound):
        _ = await repo.user_mission_update(
            id=-1, user_id="-1", obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.FINISH)
        )


# pytest tests/main/challenges/mission/db/test_user_mission.py::test_user_mission_lst -v -s
@pytest.mark.asyncio
async def test_user_mission_lst(repo: RepositoryMission, fxe_user_mission_default: MissionUser):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    user_mission_list = await repo.user_mission_lst(
        user_id=fxe_user_mission_default.user_id,
        filter_obj=MissionUserFilter(mission_id=fxe_user_mission_default.mission_id, status=OccupancyStatusEnum.ACTIVE),
        **default_kw,
    )
    assert len(user_mission_list) == 1

    user_mission = user_mission_list[0]

    assert user_mission.id is not None
    assert user_mission.user_id == fxe_user_mission_default.user_id
    assert user_mission.mission_id == fxe_user_mission_default.mission_id
    assert user_mission.status == OccupancyStatusEnum.ACTIVE

    user_mission_list = await repo.user_mission_lst(
        user_id=fxe_user_mission_default.user_id, filter_obj=MissionUserFilter(), **default_kw
    )
    assert len(user_mission_list) == 1

    user_mission_list = await repo.user_mission_lst(
        user_id=fxe_user_mission_default.user_id, filter_obj=MissionUserFilter(mission_id=-1), **default_kw
    )
    assert len(user_mission_list) == 0

    user_mission_list = await repo.user_mission_lst(
        user_id=fxe_user_mission_default.user_id,
        filter_obj=MissionUserFilter(status=OccupancyStatusEnum.FINISH),
        **default_kw,
    )
    assert len(user_mission_list) == 0
