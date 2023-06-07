import pytest

from src.core.entity.mission import MissionCommunity
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive, EntityNotFound
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_community_get import (
    MissionCommunityGetUsecase,
)


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_get.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_community_mission_entity: MissionCommunity,
):
    uc = MissionCommunityGetUsecase(uow=uow)
    res = await uc(
        user=test_user_premium_ru_entity,
        id=test_community_mission_entity.id,
        community_id=test_community_mission_entity.community_id,
    )
    mission = res.item
    assert isinstance(mission, MissionCommunity)
    assert test_community_mission_entity.id == mission.id
    assert test_community_mission_entity.community_id == mission.community_id
    assert test_community_mission_entity.mission_id == mission.mission_id
    assert test_community_mission_entity.date_start == mission.date_start
    assert test_community_mission_entity.date_close == mission.date_close
    assert test_community_mission_entity.status == mission.status


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_get.py::test_user_not_in_community -v -s
@pytest.mark.asyncio
async def test_user_not_in_community(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_community_mission_no_user_entity: MissionCommunity,
):
    uc = MissionCommunityGetUsecase(uow=uow)
    with pytest.raises(EntityNotFound):
        await uc(
            user=test_user_premium_ru_entity,
            id=test_community_mission_no_user_entity.id,
            community_id=test_community_mission_no_user_entity.community_id,
        )


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_get.py::test_user_blocked_in_community -v -s
@pytest.mark.asyncio
async def test_user_blocked_in_community(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_community_mission_user_blocked_entity: MissionCommunity,
):
    uc = MissionCommunityGetUsecase(uow=uow)
    with pytest.raises(PermissionError):
        await uc(
            user=test_user_premium_ru_entity,
            id=test_community_mission_user_blocked_entity.id,
            community_id=test_community_mission_user_blocked_entity.community_id,
        )


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_get.py::test_community_not_active -v -s
@pytest.mark.asyncio
async def test_community_not_active(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_community_mission_not_active_community_entity: MissionCommunity,
):
    uc = MissionCommunityGetUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(
            user=test_user_premium_ru_entity,
            id=test_community_mission_not_active_community_entity.id,
            community_id=test_community_mission_not_active_community_entity.community_id,
        )
