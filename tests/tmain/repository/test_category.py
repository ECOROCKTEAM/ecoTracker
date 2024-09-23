import pytest

from src.core.const.translate import DEFAULT_LANGUANGE
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.category import (
    IRepositoryOccupancyCategory,
    OccupancyFilter,
)
from tests.dataloader import dataloader


# pytest tests/tmain/repository/test_occupancy_category.py::test_get_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "language_list, language_target",
    [([LanguageEnum.RU, LanguageEnum.EN], LanguageEnum.RU), ([LanguageEnum.RU, LanguageEnum.EN], LanguageEnum.EN)],
)
async def test_get_ok(
    dl: dataloader,
    repo_category: IRepositoryOccupancyCategory,
    language_list: list[LanguageEnum],
    language_target: LanguageEnum,
):
    print()
    # Arrange
    category_model = await dl.create_category(language_list=language_list)
    # Act
    category = await repo_category.get(id=category_model.id, lang=language_target)
    # Assert
    assert category.id == category_model.id
    assert category.language == language_target


# pytest tests/tmain/repository/test_occupancy_category.py::test_get_ok_default_language -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "language_list, language_target, language_asrt",
    [
        ([LanguageEnum.EN, LanguageEnum.FR], LanguageEnum.RU, DEFAULT_LANGUANGE),
        ([LanguageEnum.EN, LanguageEnum.RU], LanguageEnum.FR, DEFAULT_LANGUANGE),
    ],
)
async def test_get_ok_default_language(
    dl: dataloader,
    repo_category: IRepositoryOccupancyCategory,
    language_list: list[LanguageEnum],
    language_target: LanguageEnum,
    language_asrt: LanguageEnum,
):
    print()
    # Arrange
    category_model = await dl.create_category(language_list=language_list)
    # Act
    category = await repo_category.get(id=category_model.id, lang=language_target)
    # Assert
    assert category.id == category_model.id
    assert category.language == language_asrt


# pytest tests/tmain/repository/test_occupancy_category.py::test_get_not_found -v -s
@pytest.mark.asyncio
# @pytest.mark.parametrize("", [])
async def test_get_not_found(dl: dataloader, repo_category: IRepositoryOccupancyCategory):
    print()
    # Arrange
    target_id = -1
    # Act & Assert
    with pytest.raises(EntityNotFound) as e:
        await repo_category.get(id=target_id, lang=LanguageEnum.RU)
    assert f"OccupancyCategory.id={target_id} not found" in str(e.value)


# pytest tests/tmain/repository/test_occupancy_category.py::test_get_not_found_translate -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "language_create, language_target", [(LanguageEnum.RU, LanguageEnum.EN), (LanguageEnum.RU, LanguageEnum.FR)]
)
async def test_get_not_found_translate(
    dl: dataloader,
    repo_category: IRepositoryOccupancyCategory,
    language_create: LanguageEnum,
    language_target: LanguageEnum,
):
    print()
    # Arrange
    category_model = await dl.create_category(language_list=[language_create])
    # Act & Assert
    with pytest.raises(TranslateNotFound) as e:
        await repo_category.get(id=category_model.id, lang=language_target)

    assert f"OccupancyCategory={category_model.id} with lang={language_target.name} not found" == str(e.value)


# pytest tests/tmain/repository/test_occupancy_category.py::test_lst_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "language_list, language_target, language_list_asrt",
    [
        ([LanguageEnum.EN, LanguageEnum.FR, LanguageEnum.RU], LanguageEnum.RU, [LanguageEnum.RU]),
        ([LanguageEnum.EN, LanguageEnum.RU], LanguageEnum.FR, [LanguageEnum.EN]),
    ],
)
async def test_lst_ok(
    dl: dataloader,
    repo_category: IRepositoryOccupancyCategory,
    language_list: list[LanguageEnum],
    language_target: LanguageEnum,
    language_list_asrt: list[LanguageEnum],
):
    print()
    # Arrange
    category_model = await dl.create_category(language_list=language_list)
    category_model2 = await dl.create_category(language_list=language_list)
    fltr = OccupancyFilter()
    # Act
    category_list = await repo_category.lst(lang=language_target, fltr=fltr)
    # Assert
    category_language_set = set([c.language for c in category_list])
    language_asrt_set = set(language_list_asrt)
    id_set = set([c.id for c in category_list])
    id_asrt_set = set([category_model.id, category_model2.id])
    assert category_language_set == language_asrt_set
    assert id_set == id_asrt_set


# pytest tests/tmain/repository/test_occupancy_category.py::test_lst_not_found_translate -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "language_list, language_target",
    [
        ([LanguageEnum.FR], LanguageEnum.RU),
        ([LanguageEnum.RU], LanguageEnum.EN),
    ],
)
async def test_lst_not_found_translate(
    dl: dataloader,
    repo_category: IRepositoryOccupancyCategory,
    language_list: list[LanguageEnum],
    language_target: LanguageEnum,
):
    print()
    # Arrange
    await dl.create_category(language_list=language_list)
    await dl.create_category(language_list=language_list)
    fltr = OccupancyFilter()
    # Act & Assert
    with pytest.raises(TranslateNotFound) as e:
        await repo_category.lst(lang=language_target, fltr=fltr)
    assert f"OccupancyCategory translate for lang={language_target.name} not found" == str(e.value)


async def _arrange_occupancy_filter_not_empty(dl: dataloader):
    category_model = await dl.create_category()
    _ = await dl.create_category()

    fltr = OccupancyFilter(id__in=[category_model.id])
    arrange_category_id_set = {
        category_model.id,
    }
    return fltr, arrange_category_id_set


async def _arrange_occupancy_filter_empty(dl: dataloader):
    category_model_1 = await dl.create_category()
    category_model_2 = await dl.create_category()

    fltr = OccupancyFilter()
    arrange_category_id_set = {category_model_1.id, category_model_2.id}
    return fltr, arrange_category_id_set


# pytest tests/tmain/repository/test_occupancy_category.py::test_lst_fltr_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_func", [_arrange_occupancy_filter_empty, _arrange_occupancy_filter_not_empty])
async def test_lst_fltr_ok(dl: dataloader, repo_category: IRepositoryOccupancyCategory, arrange_func):
    print()
    # Arrange
    fltr, arrange_occupancy_id_set = await arrange_func(dl=dl)
    # Act
    category_list = await repo_category.lst(lang=LanguageEnum.EN, fltr=fltr)
    # Assert
    id_set = set([c.id for c in category_list])
    assert id_set == arrange_occupancy_id_set
