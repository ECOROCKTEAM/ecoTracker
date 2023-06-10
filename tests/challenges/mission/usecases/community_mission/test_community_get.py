import pytest

from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.community import Community
from src.core.entity.mission import MissionCommunity
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_community_get import (
    MissionCommunityGetUsecase,
)
from tests.fixtures.challenges.mission.usecase.community_mission import (
    mock_community_mission_get,
)
from tests.fixtures.community.usecase.community import (
    mock_community_get_default,
    mock_community_get_not_active,
)
from tests.fixtures.community.usecase.user import (
    mock_community_user_get_blocked,
    mock_community_user_get_default,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_get.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_user_get_default: UserCommunityDTO,
    mock_community_mission_get: MissionCommunity,
    mock_community_get_default: Community,
):
    uc = MissionCommunityGetUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        id=1,
        community_id=1,
    )
    mission = res.item
    assert isinstance(mission, MissionCommunity)
    assert mock_community_mission_get.id == mission.id


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_get.py::test_user_blocked_in_community -v -s
@pytest.mark.asyncio
async def test_user_blocked_in_community(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_user_get_blocked: UserCommunityDTO,
    mock_community_mission_get: MissionCommunity,
    mock_community_get_default: Community,
):
    uc = MissionCommunityGetUsecase(uow=uow)
    with pytest.raises(PermissionError):
        await uc(
            user=fxe_user_default,
            id=1,
            community_id=1,
        )


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_get.py::test_community_not_active -v -s
@pytest.mark.asyncio
async def test_community_not_active(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_user_get_default: UserCommunityDTO,
    mock_community_get_not_active: Community,
):
    uc = MissionCommunityGetUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(
            user=fxe_user_default,
            id=1,
            community_id=1,
        )
