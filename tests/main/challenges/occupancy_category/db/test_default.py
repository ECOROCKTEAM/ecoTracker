import pytest

from src.core.dto.mock import MockObj
from src.core.entity.occupancy import OccupancyCategory
from src.core.entity.task import Task
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound, TranslateNotFound
from src.data.repository.challenges.occupancy_category import (
    IRepositoryOccupancyCategory,
)
from tests.fixtures.challenges.category.db.entity import (
    fxe_category_default,
    fxe_category_en,
)
from tests.fixtures.challenges.category.db.model import (
    fxm_category_default,
    fxm_category_en,
)


# pytest tests/main/challenges/occupancy_category/db/test_default.py::test_get_ok -v -s
@pytest.mark.asyncio
async def test_get_ok(repo: IRepositoryOccupancyCategory, fxe_category_default: OccupancyCategory):
    oc = await repo.get(id=fxe_category_default.id, lang=fxe_category_default.language)
    assert fxe_category_default.id == oc.id
    assert fxe_category_default.name == oc.name
    assert fxe_category_default.language == oc.language


# pytest tests/main/challenges/occupancy_category/db/test_default.py::test_not_found -v -s
@pytest.mark.asyncio
async def test_not_found(repo: IRepositoryOccupancyCategory):
    with pytest.raises(EntityNotFound):
        await repo.get(id=-1, lang=LanguageEnum.RU)


# pytest tests/main/challenges/occupancy_category/db/test_default.py::test_not_found_translate -v -s
@pytest.mark.asyncio
async def test_not_found_translate(repo: IRepositoryOccupancyCategory, fxe_category_default: OccupancyCategory):
    with pytest.raises(TranslateNotFound):
        await repo.get(id=fxe_category_default.id, lang=LanguageEnum.EN)


# pytest tests/main/challenges/occupancy_category/db/test_default.py::test_lst -v -s
@pytest.mark.asyncio
async def test_lst(
    repo: IRepositoryOccupancyCategory, fxe_category_default: OccupancyCategory, fxe_category_en: OccupancyCategory
):
    oc_list = await repo.lst(
        lang=LanguageEnum.RU,
    )
    assert len(oc_list) == 2
    for oc in oc_list:
        if oc.language == LanguageEnum.EN:
            check_oc = fxe_category_en
        elif oc.language == LanguageEnum.RU:
            check_oc = fxe_category_default
        else:
            raise ValueError("")

        assert check_oc.id == oc.id
        assert check_oc.name == oc.name
        assert check_oc.language == oc.language
