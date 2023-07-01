from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.mission import (
    MissionCommunityCreateDTO,
    MissionCommunityUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.community import Community
from src.core.entity.mission import Mission, MissionCommunity
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.challenges.mission import MissionCommunityFilter
from src.data.models.challenges.mission import CommunityMissionModel
from src.data.models.community.community import CommunityModel
from src.data.repository.challenges.mission import RepositoryMission
from tests.fixtures.challenges.category.db.model import fxm_category_default
from tests.fixtures.challenges.mission.db.community.entity import (
    fxe_community_mission_default,
)
from tests.fixtures.challenges.mission.db.community.model import (
    fxm_community_mission_default,
)
from tests.fixtures.challenges.mission.db.entity import fxe_mission_default
from tests.fixtures.challenges.mission.db.model import fxm_mission_default
from tests.fixtures.community.db.entity import fxe_community_default
from tests.fixtures.community.db.model import fxm_community_default
from tests.fixtures.user.db.model import fxm_user_default
from tests.fixtures.user_community.db.model import fxm_user_community_default


# pytest tests/main/challenges/mission/db/test_community_mission.py::test_get_community_mission_ok -v -s
@pytest.mark.asyncio
async def test_get_community_mission_ok(repo: RepositoryMission, fxe_community_mission_default: MissionCommunity):
    mission = await repo.community_mission_get(
        id=fxe_community_mission_default.id, community_id=fxe_community_mission_default.community_id
    )

    assert fxe_community_mission_default.id == mission.id
    assert fxe_community_mission_default.community_id == mission.community_id
    assert fxe_community_mission_default.mission_id == mission.mission_id
    assert fxe_community_mission_default.author == mission.author
    assert fxe_community_mission_default.date_start == mission.date_start
    assert fxe_community_mission_default.date_close == mission.date_close
    assert fxe_community_mission_default.status == mission.status


# pytest tests/main/challenges/mission/db/test_community_mission.py::test_get_community_mission_not_found -v -s
@pytest.mark.asyncio
async def test_get_community_mission_not_found(repo: RepositoryMission):
    with pytest.raises(EntityNotFound):
        _ = await repo.community_mission_get(id=-1, community_id=1)


# pytest tests/main/challenges/mission/db/test_community_mission.py::test_create_community_mission_ok -v -s
@pytest.mark.asyncio
async def test_create_community_mission_ok(
    session: AsyncSession,
    repo: RepositoryMission,
    fxe_community_default: Community,
    fxe_mission_default: Mission,
):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    community_mission_list = await repo.community_mission_lst(filter_obj=MissionCommunityFilter(), **default_kw)
    assert len(community_mission_list) == 0

    community_mission = await repo.community_mission_create(
        community_id=fxe_community_default.id,
        obj=MissionCommunityCreateDTO(mission_id=fxe_mission_default.id, author="t"),
    )
    assert community_mission.id is not None
    assert community_mission.mission_id == fxe_mission_default.id
    assert community_mission.community_id == fxe_community_default.id
    assert community_mission.author == "t"
    assert community_mission.status == OccupancyStatusEnum.ACTIVE
    assert isinstance(community_mission.date_start, datetime)
    assert community_mission.date_close is None

    create_model = await session.get(entity=CommunityMissionModel, ident={"id": community_mission.id})
    assert isinstance(create_model, CommunityMissionModel)
    await session.delete(create_model)
    await session.commit()


# pytest tests/main/challenges/mission/db/test_community_mission.py::test_create_community_mission_not_created -v -s
@pytest.mark.asyncio
async def test_create_community_mission_not_created(
    session: AsyncSession,
    repo: RepositoryMission,
    fxe_community_default: Community,
    fxe_mission_default: Mission,
):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    community_mission_list = await repo.community_mission_lst(filter_obj=MissionCommunityFilter(), **default_kw)
    assert len(community_mission_list) == 0
    with pytest.raises(EntityNotCreated):
        _ = await repo.community_mission_create(
            community_id=-1, obj=MissionCommunityCreateDTO(mission_id=fxe_mission_default.id, author="t")
        )
    await session.rollback()
    with pytest.raises(EntityNotCreated):
        _ = await repo.community_mission_create(
            community_id=fxe_community_default.id, obj=MissionCommunityCreateDTO(mission_id=-1, author="t")
        )
    await session.rollback()

    community_mission_list = await repo.community_mission_lst(filter_obj=MissionCommunityFilter(), **default_kw)
    assert len(community_mission_list) == 0


# pytest tests/main/challenges/mission/db/test_community_mission.py::test_update_community_mission_ok -v -s
@pytest.mark.asyncio
async def test_update_community_mission_ok(
    session: AsyncSession,
    repo: RepositoryMission,
    fxe_community_mission_default: MissionCommunity,
):
    assert fxe_community_mission_default.date_close is None

    updated = await repo.community_mission_update(
        id=fxe_community_mission_default.id,
        community_id=fxe_community_mission_default.community_id,
        obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
    )
    await session.commit()

    assert isinstance(updated.date_close, datetime)
    assert updated.status == OccupancyStatusEnum.FINISH

    date_after_update = updated.date_close

    updated_second = await repo.community_mission_update(
        id=fxe_community_mission_default.id,
        community_id=fxe_community_mission_default.community_id,
        obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.REJECT),
    )
    await session.commit()

    assert isinstance(updated_second.date_close, datetime)
    assert updated_second.status == OccupancyStatusEnum.REJECT
    assert updated_second.date_close > date_after_update


# pytest tests/main/challenges/mission/db/test_community_mission.py::test_update_community_mission_not_found -v -s
@pytest.mark.asyncio
async def test_update_community_mission_not_found(
    repo: RepositoryMission,
    fxe_community_mission_default: MissionCommunity,
):
    with pytest.raises(EntityNotFound):
        _ = await repo.community_mission_update(
            id=-1,
            community_id=fxe_community_mission_default.community_id,
            obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
        )
    with pytest.raises(EntityNotFound):
        _ = await repo.community_mission_update(
            id=fxe_community_mission_default.id,
            community_id=-1,
            obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
        )

    with pytest.raises(EntityNotFound):
        _ = await repo.community_mission_update(
            id=-1, community_id=-1, obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH)
        )


# pytest tests/main/challenges/mission/db/test_community_mission.py::test_community_mission_lst -v -s
@pytest.mark.asyncio
async def test_community_mission_lst(repo: RepositoryMission, fxe_community_mission_default: MissionCommunity):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    community_mission_list = await repo.community_mission_lst(
        filter_obj=MissionCommunityFilter(
            community_id_list=[fxe_community_mission_default.community_id],
            community_id=fxe_community_mission_default.community_id,
            status=OccupancyStatusEnum.ACTIVE,
        ),
        **default_kw,
    )
    assert len(community_mission_list) == 1

    community_mission = community_mission_list[0]

    assert community_mission.id is not None
    assert community_mission.community_id == fxe_community_mission_default.community_id
    assert community_mission.mission_id == fxe_community_mission_default.mission_id
    assert community_mission.status == OccupancyStatusEnum.ACTIVE

    community_mission_list = await repo.community_mission_lst(
        filter_obj=MissionCommunityFilter(),
        **default_kw,
    )
    assert len(community_mission_list) == 1

    community_mission_list = await repo.community_mission_lst(
        filter_obj=MissionCommunityFilter(mission_id=-1),
        **default_kw,
    )
    assert len(community_mission_list) == 0

    community_mission_list = await repo.community_mission_lst(
        filter_obj=MissionCommunityFilter(community_id=-1),
        **default_kw,
    )
    assert len(community_mission_list) == 0

    community_mission_list = await repo.community_mission_lst(
        filter_obj=MissionCommunityFilter(community_id_list=[]),
        **default_kw,
    )
    assert len(community_mission_list) == 0
