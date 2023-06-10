import pytest

from src.core.dto.challenges.mission import MissionUserCreateDTO
from src.core.entity.mission import Mission, MissionUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_user_create import (
    MissionUserCreateUsecase,
)
from tests.fixtures.challenges.mission.usecase.mission import (
    mock_mission_get_default,
    mock_mission_not_active,
)
from tests.fixtures.challenges.mission.usecase.user_mission import (
    mock_user_mission_create,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# python -m pytest tests/challenges/mission/usecases/user_mission/test_user_create.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_mission_get_default: Mission,
    mock_user_mission_create: MissionUser,
):
    uc = MissionUserCreateUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        create_obj=MissionUserCreateDTO(
            mission_id=1,
            status=OccupancyStatusEnum.ACTIVE,
        ),
    )
    mission = res.item
    assert isinstance(mission, MissionUser)
    assert mission.id is mock_user_mission_create.id


# python -m pytest tests/challenges/mission/usecases/user_mission/test_user_create.py::test_not_active -v -s
@pytest.mark.asyncio
async def test_not_active(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_mission_not_active: Mission,
):
    assert mock_mission_not_active.active is False
    uc = MissionUserCreateUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        _ = await uc(
            user=fxe_user_default,
            create_obj=MissionUserCreateDTO(
                mission_id=1,
                status=OccupancyStatusEnum.ACTIVE,
            ),
        )
