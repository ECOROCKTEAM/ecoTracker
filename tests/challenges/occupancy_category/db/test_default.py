import pytest

from src.core.dto.mock import MockObj
from src.core.entity.occupancy import OccupancyCategory
from src.core.entity.task import Task
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound, TranslateNotFound
from src.data.repository.challenges.occupancy_category import (
    IRepositoryOccupancyCategory,
)
from tests.fixtures.challenges.category.db.entity import fxe_category_default
from tests.fixtures.challenges.category.db.model import fxm_category_default


# pytest tests/challenges/occupancy_category/db/test_default.py::test_get_ok -v -s
@pytest.mark.asyncio
async def test_get_ok(repo: IRepositoryOccupancyCategory, fxe_category_default: OccupancyCategory):
    oc = await repo.get(id=fxe_category_default.id, lang=fxe_category_default.language)
    assert fxe_category_default.id == oc.id
    assert fxe_category_default.name == oc.name
    assert fxe_category_default.language == oc.language


# pytest tests/challenges/occupancy_category/db/test_default.py::test_not_found -v -s
@pytest.mark.asyncio
async def test_not_found(repo: IRepositoryOccupancyCategory):
    with pytest.raises(EntityNotFound):
        await repo.get(id=-1, lang=LanguageEnum.RU)


# pytest tests/challenges/occupancy_category/db/test_default.py::test_not_found_translate -v -s
@pytest.mark.asyncio
async def test_not_found_translate(repo: IRepositoryOccupancyCategory, fxe_category_default: OccupancyCategory):
    with pytest.raises(TranslateNotFound):
        await repo.get(id=fxe_category_default.id, lang=LanguageEnum.EN)


# TODO TEST LST
