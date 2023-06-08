import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.mission import MissionCommunityUpdateDTO
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.dto.mock import MockObj
from src.core.entity.mission import MissionCommunity
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotActive, EntityNotChange, EntityNotFound
from src.core.interfaces.repository.challenges.mission import MissionCommunityFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_community_update import (
    MissionCommunityUpdateUsecase,
)
from src.data.models.community.community import CommunityScoreModel


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_update.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    session: AsyncSession,
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_community_mission_user_admin_entity: MissionCommunity,
):
    uc = MissionCommunityUpdateUsecase(uow=uow)
    res = await uc(
        user=test_user_premium_ru_entity,
        id=test_community_mission_user_admin_entity.id,
        community_id=test_community_mission_user_admin_entity.community_id,
        update_obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
    )
    mission = res.item
    assert isinstance(mission, MissionCommunity)
    assert test_community_mission_user_admin_entity.id == mission.id
    assert mission.status == OccupancyStatusEnum.FINISH

    async with uow as _uow:
        base_mission = await uow.mission.get(
            id=test_community_mission_user_admin_entity.mission_id, lang=test_user_premium_ru_entity.language
        )
        user_score = await _uow.score_community.community_get(
            community_id=test_community_mission_user_admin_entity.community_id
        )
        assert user_score.value == base_mission.score
        assert base_mission.id == test_community_mission_user_admin_entity.mission_id

    await session.execute(
        delete(CommunityScoreModel).where(
            CommunityScoreModel.community_id == test_community_mission_user_admin_entity.community_id
        )
    )
    await session.commit()


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_update.py::test_not_changed -v -s
@pytest.mark.asyncio
async def test_not_changed(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_community_mission_user_admin_finished_entity: MissionCommunity,
):
    uc = MissionCommunityUpdateUsecase(uow=uow)
    with pytest.raises(EntityNotChange):
        await uc(
            user=test_user_premium_ru_entity,
            id=test_community_mission_user_admin_finished_entity.id,
            community_id=test_community_mission_user_admin_finished_entity.community_id,
            update_obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.ACTIVE),
        )


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_update.py::test_user_blocked -v -s
@pytest.mark.asyncio
async def test_user_blocked(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_community_mission_user_blocked_entity: MissionCommunity,
):
    uc = MissionCommunityUpdateUsecase(uow=uow)
    with pytest.raises(PermissionError):
        await uc(
            user=test_user_premium_ru_entity,
            id=test_community_mission_user_blocked_entity.id,
            community_id=test_community_mission_user_blocked_entity.community_id,
            update_obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
        )


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_update.py::test_community_not_active -v -s
@pytest.mark.asyncio
async def test_community_not_active(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_community_mission_not_active_community_entity: MissionCommunity,
):
    uc = MissionCommunityUpdateUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(
            user=test_user_premium_ru_entity,
            id=test_community_mission_not_active_community_entity.id,
            community_id=test_community_mission_not_active_community_entity.community_id,
            update_obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
        )
