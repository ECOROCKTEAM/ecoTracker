import pytest

from src.core.entity.mission import Mission
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_get import MissionGetUsecase


# python -m pytest tests/challenges/mission/usecases/test_get.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_mission_entity_ru: Mission,
):
    uc = MissionGetUsecase(uow=uow)
    res = await uc(user=test_user_premium_ru_entity, id=test_mission_entity_ru.id)
    mission = res.item
    assert isinstance(mission, Mission)
    assert test_mission_entity_ru.id == mission.id
    assert test_mission_entity_ru.active == mission.active
    assert test_mission_entity_ru.score == mission.score
    assert test_mission_entity_ru.description == mission.description
    assert test_mission_entity_ru.instruction == mission.instruction
    assert test_mission_entity_ru.category_id == mission.category_id
    assert test_mission_entity_ru.language == mission.language
    assert test_mission_entity_ru.language == test_user_premium_ru_entity.language


# python -m pytest tests/challenges/mission/usecases/test_get.py::test_not_active -v -s
@pytest.mark.asyncio
async def test_not_active(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_mission_entity_not_active: Mission,
):
    assert test_mission_entity_not_active.active is False
    uc = MissionGetUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        _ = await uc(user=test_user_premium_ru_entity, id=test_mission_entity_not_active.id)
