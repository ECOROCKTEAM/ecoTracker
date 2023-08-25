import pytest

from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.group import Group
from src.core.entity.mission import MissionGroup
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_group_get import (
    MissionGroupGetUsecase,
)
from tests.fixtures.challenges.mission.usecase.group_mission import (
    mock_group_mission_get,
)
from tests.fixtures.group.usecase.group import (
    mock_group_get_default,
    mock_group_get_not_active,
)
from tests.fixtures.group.usecase.user import (
    mock_group_user_get_blocked,
    mock_group_user_get_default,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/challenges/mission/usecases/group_mission/test_group_get.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_user_get_default: UserGroupDTO,
    mock_group_mission_get: MissionGroup,
    mock_group_get_default: Group,
):
    uc = MissionGroupGetUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        id=1,
        group_id=1,
    )
    mission = res.item
    assert isinstance(mission, MissionGroup)
    assert mock_group_mission_get.id == mission.id


# pytest tests/main/challenges/mission/usecases/group_mission/test_group_get.py::test_user_blocked_in_group -v -s
@pytest.mark.asyncio
async def test_user_blocked_in_group(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_user_get_blocked: UserGroupDTO,
    mock_group_mission_get: MissionGroup,
    mock_group_get_default: Group,
):
    uc = MissionGroupGetUsecase(uow=uow)
    with pytest.raises(PermissionError):
        await uc(
            user=fxe_user_default,
            id=1,
            group_id=1,
        )


# pytest tests/main/challenges/mission/usecases/group_mission/test_group_get.py::test_group_not_active -v -s
@pytest.mark.asyncio
async def test_group_not_active(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_user_get_default: UserGroupDTO,
    mock_group_get_not_active: Group,
):
    uc = MissionGroupGetUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(
            user=fxe_user_default,
            id=1,
            group_id=1,
        )
