import stat
from dataclasses import asdict
from unittest.mock import Mock

import pytest

from src.core.dto.challenges.mission import (
    MissionCommunityCreateDTO,
    MissionCommunityUpdateDTO,
    MissionUserCreateDTO,
    MissionUserUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.community import Community
from src.core.entity.mission import Mission, MissionCommunity, MissionUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.challenges.mission import (
    MissionCommunityFilter,
    MissionFilter,
    MissionUserFilter,
)
from src.data.models.challenges.mission import (
    CommunityMissionModel,
    MissionModel,
    UserMissionModel,
)
from src.data.unit_of_work import SqlAlchemyUnitOfWork

# python -m pytest tests/db/test_mission.py -v -s


# python -m pytest tests/db/test_mission.py::test_get -v -s
@pytest.mark.asyncio
async def test_get(pool, test_mission: Mission):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        mission = await uow.mission.get(id=test_mission.id, lang=test_mission.language)
    assert test_mission.id == mission.id
    assert test_mission.active == mission.active
    assert test_mission.score == mission.score
    assert test_mission.description == mission.description
    assert test_mission.instruction == mission.instruction
    assert test_mission.category_id == mission.category_id
    assert test_mission.language == mission.language


# python -m pytest tests/db/test_mission.py::test_get_error -v -s
@pytest.mark.asyncio
async def test_get_error(pool):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        with pytest.raises(EntityNotFound):
            _ = await uow.mission.get(id=-1, lang=LanguageEnum.RU)


# python -m pytest tests/db/test_mission.py::test_lst -v -s
@pytest.mark.asyncio
async def test_lst(pool, test_mission_model_list: list[MissionModel]):
    lang = LanguageEnum.RU
    filter_obj = MissionFilter()
    test_mission_ids = [m.id for m in test_mission_model_list]
    async with SqlAlchemyUnitOfWork(pool) as uow:
        mission_list = await uow.mission.lst(
            filter_obj=filter_obj,
            lang=lang,
            order_obj=MockObj(),
            pagination_obj=MockObj(),
        )
    assert len(test_mission_model_list) != 0
    assert len(mission_list) != 0
    for mission in mission_list:
        assert mission.id in test_mission_ids
        assert mission.language == lang


# python -m pytest tests/db/test_mission.py::test_user_mission_get -v -s
@pytest.mark.asyncio
async def test_user_mission_get(pool, test_user_mission: MissionUser):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        mission_user = await uow.mission.user_mission_get(
            user_id=test_user_mission.user_id,
            mission_id=test_user_mission.mission_id,
        )
    assert test_user_mission.user_id == mission_user.user_id
    assert test_user_mission.mission_id == mission_user.mission_id
    assert test_user_mission.status == mission_user.status


# python -m pytest tests/db/test_mission.py::test_user_mission_create -v -s
@pytest.mark.asyncio
async def test_user_mission_create(pool, test_user_2: User, test_mission: Mission):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        mission_user_lst = await uow.mission.user_mission_lst(
            user_id=test_user_2.id, filter_obj=MissionUserFilter(), order_obj=MockObj(), pagination_obj=MockObj()
        )
        stlen = len(mission_user_lst)
        mission_user_created = await uow.mission.user_mission_create(
            user_id=test_user_2.id,
            obj=MissionUserCreateDTO(mission_id=test_mission.id, status=OccupancyStatusEnum.ACTIVE),
        )
        await uow.commit()

        assert mission_user_created.user_id == test_user_2.id
        assert mission_user_created.mission_id == test_mission.id
        assert mission_user_created.status == OccupancyStatusEnum.ACTIVE
        mission_user_lst = await uow.mission.user_mission_lst(
            user_id=test_user_2.id, filter_obj=MissionUserFilter(), order_obj=MockObj(), pagination_obj=MockObj()
        )
        enlen = len(mission_user_lst)
        assert enlen > stlen


# python -m pytest tests/db/test_mission.py::test_user_mission_update -v -s
@pytest.mark.asyncio
async def test_user_mission_update(pool, test_user_mission: MissionUser):
    current_status = test_user_mission.status
    new_status = [s for s in OccupancyStatusEnum if s != current_status][0]
    async with SqlAlchemyUnitOfWork(pool) as uow:
        mission_user = await uow.mission.user_mission_update(
            user_id=test_user_mission.user_id,
            mission_id=test_user_mission.mission_id,
            obj=MissionUserUpdateDTO(status=new_status),
        )
        await uow.commit()

        assert mission_user.user_id == test_user_mission.user_id
        assert mission_user.mission_id == test_user_mission.mission_id
        assert mission_user.status == new_status
        assert new_status != current_status


# python -m pytest tests/db/test_mission.py::test_user_mission_lst -v -s
@pytest.mark.asyncio
async def test_user_mission_lst(pool, test_user: User, test_user_mission_model_list: list[UserMissionModel]):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        mission_list = await uow.mission.user_mission_lst(
            user_id=test_user.id,
            filter_obj=MissionUserFilter(),
            order_obj=MockObj(),
            pagination_obj=MockObj(),
        )
    mission_user_ids = [m.user_id for m in test_user_mission_model_list]
    mission_mission_ids = [m.mission_id for m in test_user_mission_model_list]
    assert len(test_user_mission_model_list) != 0
    assert len(mission_list) != 0
    for test_mission in test_user_mission_model_list:
        assert test_mission.user_id in mission_user_ids
        assert test_mission.mission_id in mission_mission_ids


# python -m pytest tests/db/test_mission.py::test_community_mission_get -v -s
@pytest.mark.asyncio
async def test_community_mission_get(pool, test_community_mission: MissionCommunity):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        mission_user = await uow.mission.community_mission_get(
            community_id=test_community_mission.community_id,
            mission_id=test_community_mission.mission_id,
        )
    assert test_community_mission.community_id == mission_user.community_id
    assert test_community_mission.mission_id == mission_user.mission_id
    assert test_community_mission.status == mission_user.status


# python -m pytest tests/db/test_mission.py::test_community_mission_create -v -s
@pytest.mark.asyncio
async def test_community_mission_create(pool, test_community_2: Community, test_mission: Mission):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        community_mission_lst = await uow.mission.community_mission_lst(
            filter_obj=MissionCommunityFilter(), order_obj=MockObj(), pagination_obj=MockObj()
        )
        stlen = len(community_mission_lst)
        mission_community_created = await uow.mission.community_mission_create(
            obj=MissionCommunityCreateDTO(
                community_id=test_community_2.id,
                mission_id=test_mission.id,
                status=OccupancyStatusEnum.ACTIVE,
                author="amogus",
            )
        )
        await uow.commit()

        assert mission_community_created.community_id == test_community_2.id
        assert mission_community_created.mission_id == test_mission.id
        assert mission_community_created.status == OccupancyStatusEnum.ACTIVE
        community_mission_lst = await uow.mission.community_mission_lst(
            filter_obj=MissionCommunityFilter(), order_obj=MockObj(), pagination_obj=MockObj()
        )
        enlen = len(community_mission_lst)
        assert enlen > stlen


# python -m pytest tests/db/test_mission.py::test_community_mission_update -v -s
@pytest.mark.asyncio
async def test_community_mission_update(pool, test_community_mission: MissionCommunity):
    current_status = test_community_mission.status
    new_status = [s for s in OccupancyStatusEnum if s != current_status][0]
    async with SqlAlchemyUnitOfWork(pool) as uow:
        mission_community = await uow.mission.community_mission_update(
            community_id=test_community_mission.community_id,
            mission_id=test_community_mission.mission_id,
            obj=MissionCommunityUpdateDTO(status=new_status),
        )
        await uow.commit()

        assert mission_community.community_id == test_community_mission.community_id
        assert mission_community.mission_id == test_community_mission.mission_id
        assert mission_community.status == new_status
        assert new_status != current_status


# python -m pytest tests/db/test_mission.py::test_community_mission_lst -v -s
@pytest.mark.asyncio
async def test_community_mission_lst(pool, test_community_mission_model_list: list[CommunityMissionModel]):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        mission_list = await uow.mission.community_mission_lst(
            filter_obj=MissionCommunityFilter(),
            order_obj=MockObj(),
            pagination_obj=MockObj(),
        )
    mission_community_ids = [m.community_id for m in test_community_mission_model_list]
    mission_mission_ids = [m.mission_id for m in test_community_mission_model_list]
    assert len(test_community_mission_model_list) != 0
    assert len(mission_list) != 0
    for test_mission in test_community_mission_model_list:
        assert test_mission.community_id in mission_community_ids
        assert test_mission.mission_id in mission_mission_ids
