from time import sleep

import pytest

from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.mission import MissionFilter
from src.data.repository.challenges.mission import RepositoryMission
from tests.fixtures.challenges.category.db.entity import fxe_category_default
from tests.fixtures.challenges.category.db.model import fxm_category_default
from tests.fixtures.challenges.mission.db.entity import (
    fxe_mission_default,
    fxe_mission_en,
)
from tests.fixtures.challenges.mission.db.model import (
    fxm_mission_default,
    fxm_mission_en,
)


# python -m pytest tests/challenges/mission/db/test_mission.py::test_get_ok -v -s
@pytest.mark.asyncio
async def test_get_ok(repo: RepositoryMission, fxe_mission_default: Mission):
    mission = await repo.get(id=fxe_mission_default.id, lang=fxe_mission_default.language)
    assert fxe_mission_default.id == mission.id
    assert fxe_mission_default.name == mission.name
    assert fxe_mission_default.active == mission.active
    assert fxe_mission_default.score == mission.score
    assert fxe_mission_default.description == mission.description
    assert fxe_mission_default.instruction == mission.instruction
    assert fxe_mission_default.category_id == mission.category_id
    assert fxe_mission_default.language == mission.language


# python -m pytest tests/challenges/mission/db/test_mission.py::test_get_mission_not_found -v -s
@pytest.mark.asyncio
async def test_get_mission_not_found(repo: RepositoryMission):
    with pytest.raises(EntityNotFound):
        _ = await repo.get(id=-1, lang=LanguageEnum.RU)


# python -m pytest tests/challenges/mission/db/test_mission.py::test_get_not_translate -v -s
@pytest.mark.asyncio
async def test_get_not_translate(repo: RepositoryMission, fxe_mission_default: Mission):
    with pytest.raises(TranslateNotFound):
        _ = await repo.get(id=fxe_mission_default.id, lang=LanguageEnum.EN)


# python -m pytest tests/challenges/mission/db/test_mission.py::test_lst -v -s
@pytest.mark.asyncio
async def test_lst(repo: RepositoryMission, fxe_mission_default: Mission, fxe_mission_en: Mission):
    mission_list = await repo.lst(
        filter_obj=MissionFilter(), order_obj=MockObj(), pagination_obj=MockObj(), lang=LanguageEnum.RU
    )
    assert len(mission_list) == 2
    for mission_getted in mission_list:
        if mission_getted.language == LanguageEnum.EN:
            mission_check = fxe_mission_en
        elif mission_getted.language == LanguageEnum.RU:
            mission_check = fxe_mission_default
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


# python -m pytest tests/challenges/mission/db/test_mission.py::test_lst_filter -v -s
@pytest.mark.asyncio
async def test_lst_filter(repo: RepositoryMission, fxe_mission_default: Mission):
    default_kw = dict(order_obj=MockObj(), pagination_obj=MockObj(), lang=LanguageEnum.RU)
    mission_list = await repo.lst(filter_obj=MissionFilter(active=True), **default_kw)  # type: ignore
    assert len(mission_list) == 1
    mission = mission_list[0]
    assert fxe_mission_default.id == mission.id
    mission_list = await repo.lst(filter_obj=MissionFilter(active=False), **default_kw)  # type: ignore
    assert len(mission_list) == 0
