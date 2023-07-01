import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.mission import MissionCommunityUpdateDTO
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.dto.mock import MockObj
from src.core.entity.community import Community
from src.core.entity.mission import Mission, MissionCommunity
from src.core.entity.score import ScoreCommunity
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotActive, EntityNotChange, EntityNotFound
from src.core.interfaces.repository.challenges.mission import MissionCommunityFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_community_update import (
    MissionCommunityUpdateUsecase,
)
from src.data.models.community.community import CommunityScoreModel
from tests.fixtures.challenges.mission.usecase.community_mission import (
    mock_community_mission_get,
    mock_community_mission_status_finish,
    mock_community_mission_update,
)
from tests.fixtures.challenges.mission.usecase.mission import (
    mock_mission_get_default,
    mock_mission_not_active,
)
from tests.fixtures.community.usecase.community import (
    mock_community_get_default,
    mock_community_get_not_active,
)
from tests.fixtures.community.usecase.user import (
    mock_community_user_get_blocked,
    mock_community_user_get_default,
)
from tests.fixtures.const import DEFAULT_TEST_USECASE_COMMUNITY_ID
from tests.fixtures.score.usecase.community_score import mock_community_score_add
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/challenges/mission/usecases/community_mission/test_community_update.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_mission_get_default: Mission,
    mock_community_user_get_default: UserCommunityDTO,
    mock_community_mission_get: MissionCommunity,
    mock_community_get_default: Community,
    mock_community_mission_update: MissionCommunity,
    mock_community_score_add: ScoreCommunity,
):
    uc = MissionCommunityUpdateUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        id=1,
        community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
        update_obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
    )
    mission = res.item
    assert isinstance(mission, MissionCommunity)
    assert mock_community_mission_update.id == mission.id


# pytest tests/main/challenges/mission/usecases/community_mission/test_community_update.py::test_not_changed -v -s
@pytest.mark.asyncio
async def test_not_changed(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_user_get_default: UserCommunityDTO,
    mock_community_mission_status_finish: MissionCommunity,
    mock_community_get_default: Community,
):
    uc = MissionCommunityUpdateUsecase(uow=uow)
    with pytest.raises(EntityNotChange):
        await uc(
            user=fxe_user_default,
            id=1,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            update_obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.ACTIVE),
        )


# pytest tests/main/challenges/mission/usecases/community_mission/test_community_update.py::test_user_blocked -v -s
@pytest.mark.asyncio
async def test_user_blocked(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_user_get_blocked: UserCommunityDTO,
    mock_community_get_default: Community,
):
    uc = MissionCommunityUpdateUsecase(uow=uow)
    with pytest.raises(PermissionError):
        await uc(
            user=fxe_user_default,
            id=1,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            update_obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
        )


# pytest tests/main/challenges/mission/usecases/community_mission/test_community_update.py::test_community_not_active -v -s
@pytest.mark.asyncio
async def test_community_not_active(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_get_not_active: Community,
):
    uc = MissionCommunityUpdateUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(
            user=fxe_user_default,
            id=1,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            update_obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
        )
