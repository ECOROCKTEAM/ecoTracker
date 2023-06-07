from datetime import datetime
from typing import Tuple

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.mission import (
    MissionCommunityCreateDTO,
    MissionCommunityUpdateDTO,
    MissionUserCreateDTO,
    MissionUserUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission, MissionCommunity, MissionUser
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.mission import (
    MissionCommunityFilter,
    MissionFilter,
    MissionUserFilter,
)
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.data.models.challenges.mission import (
    CommunityMissionModel,
    MissionModel,
    MissionTranslateModel,
    UserMissionModel,
)
from src.data.models.community.community import CommunityModel
from src.data.models.user.user import UserModel
from src.data.repository.challenges.mission import RepositoryMission


# python -m pytest tests/challenges/mission/db/test_community_mission.py::test_get_community_mission_ok -v -s
@pytest.mark.asyncio
async def test_get_community_mission_ok(repo: RepositoryMission, test_community_mission_entity: MissionCommunity):
    community_mission = await repo.community_mission_get(
        id=test_community_mission_entity.id, community_id=test_community_mission_entity.community_id
    )

    assert test_community_mission_entity.id == community_mission.id
    assert test_community_mission_entity.community_id == community_mission.community_id
    assert test_community_mission_entity.mission_id == community_mission.mission_id
    assert test_community_mission_entity.author == community_mission.author
    assert test_community_mission_entity.date_start == community_mission.date_start
    assert test_community_mission_entity.date_close == community_mission.date_close
    assert test_community_mission_entity.status == community_mission.status


# python -m pytest tests/challenges/mission/db/test_community_mission.py::test_get_community_mission_not_found -v -s
@pytest.mark.asyncio
async def test_get_community_mission_not_found(repo: RepositoryMission):
    with pytest.raises(EntityNotFound):
        _ = await repo.community_mission_get(id=-1, community_id=1)


# python -m pytest tests/challenges/mission/db/test_community_mission.py::test_create_community_mission_ok -v -s
@pytest.mark.asyncio
async def test_create_community_mission_ok(
    session: AsyncSession,
    repo: RepositoryMission,
    test_community_model: CommunityModel,
    test_mission_entity_ru: Mission,
):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    community_mission_list = await repo.community_mission_lst(filter_obj=MissionCommunityFilter(), **default_kw)
    assert len(community_mission_list) == 0

    community_mission = await repo.community_mission_create(
        community_id=test_community_model.id,
        obj=MissionCommunityCreateDTO(mission_id=test_mission_entity_ru.id, author="t"),
    )
    assert community_mission.id is not None
    assert community_mission.mission_id == test_mission_entity_ru.id
    assert community_mission.community_id == test_community_model.id
    assert community_mission.author == "t"
    assert community_mission.status == OccupancyStatusEnum.ACTIVE
    assert isinstance(community_mission.date_start, datetime)
    assert community_mission.date_close is None

    create_model = await session.get(entity=CommunityMissionModel, ident={"id": community_mission.id})
    assert isinstance(create_model, CommunityMissionModel)
    await session.delete(create_model)
    await session.commit()


# python -m pytest tests/challenges/mission/db/test_community_mission.py::test_create_community_mission_not_created -v -s
@pytest.mark.asyncio
async def test_create_community_mission_not_created(
    session: AsyncSession,
    repo: RepositoryMission,
    test_community_model: CommunityModel,
    test_mission_entity_ru: Mission,
):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    community_mission_list = await repo.community_mission_lst(filter_obj=MissionCommunityFilter(), **default_kw)
    assert len(community_mission_list) == 0
    with pytest.raises(EntityNotCreated):
        _ = await repo.community_mission_create(
            community_id=-1, obj=MissionCommunityCreateDTO(mission_id=test_mission_entity_ru.id, author="t")
        )
    await session.rollback()
    await session.refresh(test_community_model)
    community_mission_list = await repo.community_mission_lst(filter_obj=MissionCommunityFilter(), **default_kw)
    assert len(community_mission_list) == 0


# python -m pytest tests/challenges/mission/db/test_community_mission.py::test_update_community_mission_ok -v -s
@pytest.mark.asyncio
async def test_update_community_mission_ok(
    session: AsyncSession,
    repo: RepositoryMission,
    test_community_mission_entity: MissionCommunity,
):
    assert test_community_mission_entity.date_close is None
    assert test_community_mission_entity.status == OccupancyStatusEnum.ACTIVE

    updated = await repo.community_mission_update(
        id=test_community_mission_entity.id,
        community_id=test_community_mission_entity.community_id,
        obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
    )
    await session.commit()

    assert isinstance(updated.date_close, datetime)
    assert updated.status == OccupancyStatusEnum.FINISH

    date_after_update = updated.date_close

    updated_second = await repo.community_mission_update(
        id=test_community_mission_entity.id,
        community_id=test_community_mission_entity.community_id,
        obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.REJECT),
    )
    await session.commit()

    assert isinstance(updated_second.date_close, datetime)
    assert updated_second.status == OccupancyStatusEnum.REJECT
    assert updated_second.date_close > date_after_update


# python -m pytest tests/challenges/mission/db/test_community_mission.py::test_update_community_mission_not_found -v -s
@pytest.mark.asyncio
async def test_update_community_mission_not_found(
    repo: RepositoryMission,
    test_community_mission_entity: MissionCommunity,
):
    with pytest.raises(EntityNotFound):
        _ = await repo.community_mission_update(
            id=-1,
            community_id=test_community_mission_entity.community_id,
            obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
        )
    with pytest.raises(EntityNotFound):
        _ = await repo.community_mission_update(
            id=test_community_mission_entity.id,
            community_id=-1,
            obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
        )

    with pytest.raises(EntityNotFound):
        _ = await repo.community_mission_update(
            id=-1, community_id=-1, obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH)
        )


# python -m pytest tests/challenges/mission/db/test_community_mission.py::test_community_mission_lst -v -s
@pytest.mark.asyncio
async def test_community_mission_lst(repo: RepositoryMission, test_community_mission_entity: MissionCommunity):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    community_mission_list = await repo.community_mission_lst(
        filter_obj=MissionCommunityFilter(
            community_id_list=[test_community_mission_entity.community_id],
            community_id=test_community_mission_entity.community_id,
            status=OccupancyStatusEnum.ACTIVE,
        ),
        **default_kw,
    )
    assert len(community_mission_list) == 1

    community_mission = community_mission_list[0]

    assert community_mission.id is not None
    assert community_mission.community_id == test_community_mission_entity.community_id
    assert community_mission.mission_id == test_community_mission_entity.mission_id
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
