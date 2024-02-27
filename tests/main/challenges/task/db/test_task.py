import pytest

from src.core.dto.mock import MockObj
from src.core.dto.utils import IterableObj, SortObj
from src.core.entity.task import Task
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.task import TaskFilter
from src.data.repository.challenges.task import IRepositoryTask
from tests.fixtures.challenges.category.db.entity import fxe_category_default
from tests.fixtures.challenges.category.db.model import fxm_category_default
from tests.fixtures.challenges.task.db.entity import fxe_task_default, fxe_task_en
from tests.fixtures.challenges.task.db.model import fxm_task_default, fxm_task_en


# pytest tests/main/challenges/task/db/test_task.py::test_get_ok -v -s
@pytest.mark.asyncio
async def test_get_ok(repo: IRepositoryTask, fxe_task_default: Task):
    task = await repo.get(id=fxe_task_default.id, lang=fxe_task_default.language)
    assert fxe_task_default.id == task.id
    assert fxe_task_default.name == task.name
    assert fxe_task_default.active == task.active
    assert fxe_task_default.score == task.score
    assert fxe_task_default.description == task.description
    assert fxe_task_default.category_id == task.category_id
    assert fxe_task_default.language == task.language


# pytest tests/main/challenges/task/db/test_task.py::test_get_task_not_found -v -s
@pytest.mark.asyncio
async def test_get_task_not_found(repo: IRepositoryTask):
    with pytest.raises(EntityNotFound):
        _ = await repo.get(id=-1, lang=LanguageEnum.RU)


# pytest tests/main/challenges/task/db/test_task.py::test_get_not_translate -v -s
@pytest.mark.asyncio
async def test_get_not_translate(repo: IRepositoryTask, fxe_task_default: Task):
    with pytest.raises(TranslateNotFound):
        _ = await repo.get(id=fxe_task_default.id, lang=LanguageEnum.EN)


# pytest tests/main/challenges/task/db/test_task.py::test_lst -v -s
@pytest.mark.asyncio
async def test_lst(repo: IRepositoryTask, fxe_task_default: Task, fxe_task_en: Task):
    task_list_pagination = await repo.lst(
        filter_obj=TaskFilter(),
        sorting_obj=SortObj(),
        iterable_obj=IterableObj(),
        lang=LanguageEnum.RU,
    )
    task_list = task_list_pagination.items
    assert len(task_list) == 2
    for task_getted in task_list:
        if task_getted.language == LanguageEnum.EN:
            task_check = fxe_task_en
        elif task_getted.language == LanguageEnum.RU:
            task_check = fxe_task_default
        else:
            raise ValueError("")

        assert task_check.id == task_getted.id
        assert task_check.name == task_getted.name
        assert task_check.active == task_getted.active
        assert task_check.score == task_getted.score
        assert task_check.description == task_getted.description
        assert task_check.category_id == task_getted.category_id
        assert task_check.language == task_getted.language


# pytest tests/main/challenges/task/db/test_task.py::test_lst_filter -v -s
@pytest.mark.asyncio
async def test_lst_filter(repo: IRepositoryTask, fxe_task_default: Task):
    default_kw = dict(order_obj=MockObj(), pagination_obj=MockObj(), lang=LanguageEnum.RU)
    task_list_pagination = await repo.lst(filter_obj=TaskFilter(active=True), **default_kw)  # type: ignore
    task_list = task_list_pagination.items
    assert len(task_list) == 1
    task = task_list[0]
    assert fxe_task_default.id == task.id

    task_list_pagination = await repo.lst(filter_obj=TaskFilter(active=False), **default_kw)  # type: ignore
    assert len(task_list) == 0

    task_list_pagination = await repo.lst(filter_obj=TaskFilter(category_id=-1), **default_kw)  # type: ignore
    assert len(task_list) == 0
