import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.mission import MissionGroupUpdateDTO
from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.dto.mock import MockObj
from src.core.entity.group import Group
from src.core.entity.mission import Mission, MissionGroup
from src.core.entity.score import ScoreGroup
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotActive, EntityNotChange, EntityNotFound
from src.core.interfaces.repository.challenges.mission import MissionGroupFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_group_update import (
    MissionGroupUpdateUsecase,
)
from src.data.models.group.group import GroupScoreModel
from tests.fixtures.challenges.mission.usecase.group_mission import (
    mock_group_mission_get,
    mock_group_mission_status_finish,
    mock_group_mission_update,
)
from tests.fixtures.challenges.mission.usecase.mission import (
    mock_mission_get_default,
    mock_mission_not_active,
)
from tests.fixtures.const import DEFAULT_TEST_USECASE_GROUP_ID
from tests.fixtures.group.usecase.group import (
    mock_group_get_default,
    mock_group_get_not_active,
)
from tests.fixtures.group.usecase.user import (
    mock_group_user_get_blocked,
    mock_group_user_get_default,
)
from tests.fixtures.score.usecase.group_score import mock_group_score_add
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/challenges/mission/usecases/group_mission/test_group_update.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_mission_get_default: Mission,
    mock_group_user_get_default: UserGroupDTO,
    mock_group_mission_get: MissionGroup,
    mock_group_get_default: Group,
    mock_group_mission_update: MissionGroup,
    mock_group_score_add: ScoreGroup,
):
    uc = MissionGroupUpdateUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        id=1,
        group_id=DEFAULT_TEST_USECASE_GROUP_ID,
        update_obj=MissionGroupUpdateDTO(status=OccupancyStatusEnum.FINISH),
    )
    mission = res.item
    assert isinstance(mission, MissionGroup)
    assert mock_group_mission_update.id == mission.id


# pytest tests/main/challenges/mission/usecases/group_mission/test_group_update.py::test_not_changed -v -s
@pytest.mark.asyncio
async def test_not_changed(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_user_get_default: UserGroupDTO,
    mock_group_mission_status_finish: MissionGroup,
    mock_group_get_default: Group,
):
    uc = MissionGroupUpdateUsecase(uow=uow)
    with pytest.raises(EntityNotChange):
        await uc(
            user=fxe_user_default,
            id=1,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            update_obj=MissionGroupUpdateDTO(status=OccupancyStatusEnum.ACTIVE),
        )


# pytest tests/main/challenges/mission/usecases/group_mission/test_group_update.py::test_user_blocked -v -s
@pytest.mark.asyncio
async def test_user_blocked(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_user_get_blocked: UserGroupDTO,
    mock_group_get_default: Group,
):
    uc = MissionGroupUpdateUsecase(uow=uow)
    with pytest.raises(PermissionError):
        await uc(
            user=fxe_user_default,
            id=1,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            update_obj=MissionGroupUpdateDTO(status=OccupancyStatusEnum.FINISH),
        )


# pytest tests/main/challenges/mission/usecases/group_mission/test_group_update.py::test_group_not_active -v -s
@pytest.mark.asyncio
async def test_group_not_active(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_not_active: Group,
):
    uc = MissionGroupUpdateUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(
            user=fxe_user_default,
            id=1,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            update_obj=MissionGroupUpdateDTO(status=OccupancyStatusEnum.FINISH),
        )
