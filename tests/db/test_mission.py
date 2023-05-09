import pytest
from dataclasses import asdict
from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.challenges.mission import MissionFilter
from src.data.unit_of_work import SqlAlchemyUnitOfWork

# python -m pytest tests/db/test_mission.py -v -s


# python -m pytest tests/db/test_mission.py::test_get -v -s
@pytest.mark.asyncio
async def test_get(pool, test_mission: Mission):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        mission = await uow.mission.get(id=test_mission.id, lang=test_mission.language)
    assert test_mission.id == mission.id
    assert test_mission.active == mission.active
    assert test_mission.score == mission.score
    assert test_mission.description == mission.description
    assert test_mission.instruction == mission.instruction
    assert test_mission.language == mission.language

    test_category = test_mission.category
    category = mission.category
    assert test_category.id == category.id
    assert test_category.name == category.name
    assert test_category.language == category.language
    assert category.language == mission.language


# python -m pytest tests/db/test_mission.py::test_get_error -v -s
@pytest.mark.asyncio
async def test_get_error(pool):
    async with SqlAlchemyUnitOfWork(pool) as uow:
        with pytest.raises(EntityNotFound):
            _ = await uow.mission.get(id=-1, lang=LanguageEnum.RU)


# python -m pytest tests/db/test_mission.py::test_lst -v -s
@pytest.mark.asyncio
async def test_lst(pool, test_mission_model_list):
    lang = LanguageEnum.RU
    filter_obj = MissionFilter()
    test_mission_ids = [m.id for m in test_mission_model_list]
    async with SqlAlchemyUnitOfWork(pool) as uow:
        mission_list = await uow.mission.lst(
            filter_obj=filter_obj,
            lang=lang,
            order_obj=MockObj(),
            pagination_obj=MockObj(),
        )
    assert len(test_mission_model_list) != 0
    assert len(mission_list) != 0
    for mission in mission_list:
        assert mission.id in test_mission_ids
        assert mission.language == lang
        assert mission.category.language == lang
