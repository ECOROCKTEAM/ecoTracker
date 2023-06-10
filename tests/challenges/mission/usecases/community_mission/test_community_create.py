import pytest

from src.core.dto.challenges.mission import MissionCommunityCreateDTO
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.community import Community
from src.core.entity.mission import Mission, MissionCommunity
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_community_create import (
    MissionCommunityCreateUsecase,
)
from tests.fixtures.challenges.mission.usecase.community_mission import (
    mock_community_mission_create,
    mock_community_mission_get,
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
from tests.fixtures.user.usecase.entity import fxe_user_default


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_create.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_mission_get_default: Mission,
    mock_community_user_get_default: UserCommunityDTO,
    mock_community_mission_get: MissionCommunity,
    mock_community_get_default: Community,
    mock_community_mission_create: MissionCommunity,
):
    uc = MissionCommunityCreateUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        community_id=1,
        create_obj=MissionCommunityCreateDTO(
            mission_id=1,
            author="n",
        ),
    )
    mission = res.item
    assert isinstance(mission, MissionCommunity)
    assert mission.id == mock_community_mission_create.id


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_create.py::test_user_incorrect_role -v -s
@pytest.mark.asyncio
async def test_user_incorrect_role(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_user_get_blocked: UserCommunityDTO,
):
    uc = MissionCommunityCreateUsecase(uow=uow)
    with pytest.raises(PermissionError):
        await uc(
            user=fxe_user_default,
            community_id=1,
            create_obj=MissionCommunityCreateDTO(
                mission_id=1,
                author="n",
            ),
        )


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_create.py::test_community_not_active -v -s
@pytest.mark.asyncio
async def test_community_not_active(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_mission_get_default: Mission,
    mock_community_user_get_default: UserCommunityDTO,
    mock_community_get_not_active: Community,
):
    uc = MissionCommunityCreateUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(
            user=fxe_user_default,
            community_id=1,
            create_obj=MissionCommunityCreateDTO(
                mission_id=1,
                author="n",
            ),
        )


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_create.py::test_mission_not_active -v -s
@pytest.mark.asyncio
async def test_mission_not_active(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_mission_not_active: Mission,
    mock_community_user_get_default: UserCommunityDTO,
    mock_community_mission_get: MissionCommunity,
    mock_community_get_default: Community,
):
    uc = MissionCommunityCreateUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(
            user=fxe_user_default,
            community_id=1,
            create_obj=MissionCommunityCreateDTO(
                mission_id=1,
                author="n",
            ),
        )
