import pytest

from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.dto.mock import MockObj
from src.core.entity.mission import MissionCommunity
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive, EntityNotFound
from src.core.interfaces.repository.challenges.mission import MissionCommunityFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_community_list import (
    MissionCommunityListUsecase,
)


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_list.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_community_mission_entity: MissionCommunity,
):
    uc = MissionCommunityListUsecase(uow=uow)
    res = await uc(
        user=test_user_premium_ru_entity,
        filter_obj=MissionCommunityFilter(),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    mission_list = res.item
    assert len(mission_list) == 1
    mission = mission_list[0]
    assert isinstance(mission, MissionCommunity)
    assert test_community_mission_entity.id == mission.id
    assert test_community_mission_entity.community_id == mission.community_id
    assert test_community_mission_entity.mission_id == mission.mission_id
    assert test_community_mission_entity.date_start == mission.date_start
    assert test_community_mission_entity.date_close == mission.date_close
    assert test_community_mission_entity.status == mission.status


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_list.py::test_user_blocked -v -s
@pytest.mark.asyncio
async def test_user_blocked(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_community_mission_user_blocked_entity: MissionCommunity,
):
    uc = MissionCommunityListUsecase(uow=uow)
    res = await uc(
        user=test_user_premium_ru_entity,
        filter_obj=MissionCommunityFilter(),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    mission_list = res.item
    assert len(mission_list) == 0


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_list.py::test_community_not_active -v -s
@pytest.mark.asyncio
async def test_community_not_active(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_community_mission_not_active_community_entity: MissionCommunity,
):
    uc = MissionCommunityListUsecase(uow=uow)
    res = await uc(
        user=test_user_premium_ru_entity,
        filter_obj=MissionCommunityFilter(),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    mission_list = res.item
    assert len(mission_list) == 0
