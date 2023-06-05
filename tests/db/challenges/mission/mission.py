import pytest

from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.mission import MissionFilter
from src.data.repository.challenges.mission import RepositoryMission


# python -m pytest tests/db/challenges/mission/mission.py::test_get_ok -v -s
@pytest.mark.asyncio
async def test_get_ok(repo: RepositoryMission, test_mission_entity_ru: Mission):
    mission_getted = await repo.get(id=test_mission_entity_ru.id, lang=test_mission_entity_ru.language)
    assert test_mission_entity_ru.id == mission_getted.id
    assert test_mission_entity_ru.name == mission_getted.name
    assert test_mission_entity_ru.active == mission_getted.active
    assert test_mission_entity_ru.score == mission_getted.score
    assert test_mission_entity_ru.description == mission_getted.description
    assert test_mission_entity_ru.instruction == mission_getted.instruction
    assert test_mission_entity_ru.category_id == mission_getted.category_id
    assert test_mission_entity_ru.language == mission_getted.language


# python -m pytest tests/db/challenges/mission/mission.py::test_get_mission_not_found -v -s
@pytest.mark.asyncio
async def test_get_mission_not_found(repo: RepositoryMission):
    with pytest.raises(EntityNotFound):
        _ = await repo.get(id=-1, lang=LanguageEnum.RU)


# python -m pytest tests/db/challenges/mission/mission.py::test_get_not_translate -v -s
@pytest.mark.asyncio
async def test_get_not_translate(repo: RepositoryMission, test_mission_entity_ru: Mission):
    with pytest.raises(TranslateNotFound):
        _ = await repo.get(id=test_mission_entity_ru.id, lang=LanguageEnum.EN)


# python -m pytest tests/db/challenges/mission/mission.py::test_lst -v -s
@pytest.mark.asyncio
async def test_lst(repo: RepositoryMission, test_mission_entity_ru: Mission, test_mission_entity_en: Mission):
    mission_list = await repo.lst(
        filter_obj=MissionFilter(), order_obj=MockObj(), pagination_obj=MockObj(), lang=LanguageEnum.RU
    )
    for mission_getted in mission_list:
        if mission_getted.language == LanguageEnum.EN:
            mission_check = test_mission_entity_en
        elif mission_getted.language == LanguageEnum.RU:
            mission_check = test_mission_entity_ru
        else:
            raise ValueError("")

        assert mission_check.id == mission_getted.id
        assert mission_check.name == mission_getted.name
        assert mission_check.active == mission_getted.active
        assert mission_check.score == mission_getted.score
        assert mission_check.description == mission_getted.description
        assert mission_check.instruction == mission_getted.instruction
        assert mission_check.category_id == mission_getted.category_id
        assert mission_check.language == mission_getted.language


# python -m pytest tests/db/challenges/mission/mission.py::test_lst_filter -v -s
@pytest.mark.asyncio
async def test_lst_filter(repo: RepositoryMission, test_mission_entity_ru: Mission):
    default_kw = dict(order_obj=MockObj(), pagination_obj=MockObj(), lang=LanguageEnum.RU)
    mission_list = await repo.lst(filter_obj=MissionFilter(active=True), **default_kw)  # type: ignore
    assert len(mission_list) == 1
    mission_list = await repo.lst(filter_obj=MissionFilter(active=False), **default_kw)  # type: ignore
    assert len(mission_list) == 0
