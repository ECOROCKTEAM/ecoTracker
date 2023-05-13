import pytest

from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission
from src.core.entity.user import User
from src.core.enum.language import LanguageEnum
from src.core.interfaces.repository.challenges.mission import MissionFilter
from src.core.usecases.challenges.mission import mission_get, mission_list
from src.data.models.challenges.mission import MissionModel
from src.data.unit_of_work import SqlAlchemyUnitOfWork


# python -m pytest tests/use_cases/test_mission.py::test_list -v -s
@pytest.mark.asyncio
async def test_list(pool, test_user: User, test_mission_model_list: list[MissionModel]):
    lang = LanguageEnum.RU
    test_mission_ids = [m.id for m in test_mission_model_list]
    test_user.language = lang
    uow = SqlAlchemyUnitOfWork(pool)
    uc = mission_list.MissionListUsecase(uow=uow)
    res = await uc(user=test_user, filter_obj=MissionFilter(), order_obj=MockObj(), pagination_obj=MockObj())
    assert isinstance(res.item, list)
    for mission in res.item:
        assert mission.id in test_mission_ids
        assert mission.language == lang


# python -m pytest tests/use_cases/test_mission.py::test_get -v -s
@pytest.mark.asyncio
async def test_get(pool, test_user: User, test_mission: Mission):
    test_user.language = test_mission.language
    uow = SqlAlchemyUnitOfWork(pool)
    uc = mission_get.MissionGetUsecase(uow=uow)
    res = await uc(user=test_user, id=test_mission.id)
    mission = res.item
    assert test_mission.id == mission.id
    assert test_mission.active == mission.active
    assert test_mission.score == mission.score
    assert test_mission.description == mission.description
    assert test_mission.instruction == mission.instruction
    assert test_mission.category_id == mission.category_id
    assert test_mission.language == mission.language
