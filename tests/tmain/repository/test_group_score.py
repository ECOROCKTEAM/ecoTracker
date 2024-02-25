import random
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from uuid import uuid4

import pytest
from sqlalchemy import func, select

from src.core.dto.group.score import GroupRatingDTO
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.score.group import IRepositoryGroupScore
from src.data.models.group.group import GroupModel, GroupScoreModel
from src.data.repository.score.group_score import calc_bounds
from tests.dataloader import dataloader
from tests.utils import catchtime

GROUP_COUNT = 1_000
GROUP_ROWS_COUNT = 10


@asynccontextmanager
async def _arrange_func(dl: dataloader, group_count: int, group_rows_count: int) -> AsyncGenerator[int, None]:
    """Prepare score / rating
    return random group_id
    """
    group_models = []
    for _ in range(group_count):
        group = GroupModel(
            name=str(uuid4()),
            description="",
            active=True,
            privacy=GroupPrivacyEnum.PUBLIC,
        )
        group_models.append(group)
    dl.session.add_all(group_models)
    await dl.session.flush()

    score_models = []
    for group in group_models:
        for _ in range(group_rows_count):
            operation = random.choice([ScoreOperationEnum.MINUS, ScoreOperationEnum.PLUS])
            value = random.randint(50, 1000)
            score = GroupScoreModel(group_id=group.id, operation=operation, value=value)
            score_models.append(score)
    dl.session.add_all(score_models)
    await dl.session.commit()

    stmt = select(func.count(GroupScoreModel.id))
    count = await dl.session.scalar(stmt)
    assert count == group_count * group_rows_count
    group_id = random.choice(group_models).id
    yield group_id

    for score in score_models:
        await dl.session.delete(score)
    await dl.session.flush()
    for group in group_models:
        await dl.session.delete(group)
    await dl.session.commit()


@asynccontextmanager
async def _arrange_func_group_with_zero_rows_score(
    dl: dataloader,
) -> AsyncGenerator[int, None]:
    group = GroupModel(
        name=str(uuid4()),
        description="",
        active=True,
        privacy=GroupPrivacyEnum.PUBLIC,
    )
    dl.session.add(group)
    await dl.session.commit()

    yield group.id

    await dl.session.delete(group)
    await dl.session.commit()


async def _assert_func_score(dl: dataloader, group_id: int) -> int:
    stmt = select(GroupScoreModel).where(GroupScoreModel.group_id == group_id)
    raw_result_list = await dl.session.scalars(stmt)
    raw_result = GroupRatingDTO(group_id=group_id, score=0, position=0)
    for obj in raw_result_list:
        if obj.operation == ScoreOperationEnum.PLUS:
            raw_result.score += obj.value
        elif obj.operation == ScoreOperationEnum.MINUS:
            raw_result.score -= obj.value
    return raw_result.score


# pytest tests/tmain/repository/test_group_score.py::test_get_rating -v -s
@pytest.mark.asyncio
async def test_get_rating(dl: dataloader, repo_group_score: IRepositoryGroupScore):
    print()
    # Arrange
    async with _arrange_func(dl=dl, group_count=GROUP_COUNT, group_rows_count=GROUP_ROWS_COUNT) as group_id:
        # Act
        with catchtime("repo:"):
            result = await repo_group_score.get_rating(group_id=group_id)
        with catchtime("raw:"):
            score = await _assert_func_score(dl=dl, group_id=group_id)

    # Assert
    assert result.position > 0
    assert result.score == score
    assert result.group_id == group_id


# pytest tests/tmain/repository/test_group_score.py::test_get_score -v -s
@pytest.mark.asyncio
async def test_get_score(dl: dataloader, repo_group_score: IRepositoryGroupScore):
    print()
    # Arrange
    async with _arrange_func(dl=dl, group_count=GROUP_COUNT, group_rows_count=GROUP_ROWS_COUNT) as group_id:
        # Act
        with catchtime("repo:"):
            result = await repo_group_score.get_score(group_id=group_id)
        with catchtime("raw:"):
            score = await _assert_func_score(dl=dl, group_id=group_id)

    # Assert
    assert result.score == score
    assert result.group_id == group_id


# pytest tests/tmain/repository/test_group_score.py::test_get_score_zero_rows_score -v -s
@pytest.mark.asyncio
async def test_get_score_zero_rows_score(dl: dataloader, repo_group_score: IRepositoryGroupScore):
    print()
    # Arrange
    async with _arrange_func_group_with_zero_rows_score(
        dl=dl,
    ) as group_id:
        # Act
        with catchtime("repo:"):
            result = await repo_group_score.get_score(group_id=group_id)
        with catchtime("raw:"):
            score = await _assert_func_score(dl=dl, group_id=group_id)

    # Assert
    assert result.score == score
    assert result.score == 0
    assert result.group_id == group_id


# pytest tests/tmain/repository/test_group_score.py::test_get_score_not_found_group_fail -v -s
@pytest.mark.asyncio
async def test_get_score_not_found_group_fail(dl: dataloader, repo_group_score: IRepositoryGroupScore):
    print()
    group_id = -1

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_group_score.get_score(group_id=group_id)


# pytest tests/tmain/repository/test_group_score.py::test_get_rating_not_found_group_fail -v -s
@pytest.mark.asyncio
async def test_get_rating_not_found_group_fail(dl: dataloader, repo_group_score: IRepositoryGroupScore):
    print()
    group_id = -1

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_group_score.get_rating(group_id=group_id)


# pytest tests/tmain/repository/test_group_score.py::test_get_rating_window -v -s
@pytest.mark.asyncio
async def test_get_rating_window(dl: dataloader, repo_group_score: IRepositoryGroupScore):
    print()
    # Arrange
    window_offset = 10
    async with _arrange_func(dl=dl, group_count=GROUP_COUNT, group_rows_count=GROUP_ROWS_COUNT) as group_id:
        # Act
        result = await repo_group_score.get_rating_window(
            window_offset=window_offset, group_id=group_id, group_privacy__in=[]
        )
    # Assert
    group_id_set = {item.group_id for item in result}
    assert group_id in group_id_set
    assert len(result) == window_offset * 2 + 1


# pytest tests/tmain/repository/test_group_score.py::test_get_rating_top -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("size", [10, 20, 50])
async def test_get_rating_top(dl: dataloader, repo_group_score: IRepositoryGroupScore, size: int):
    print()
    # Arrange
    async with _arrange_func(dl=dl, group_count=GROUP_COUNT, group_rows_count=GROUP_ROWS_COUNT):
        # Act
        result = await repo_group_score.get_rating_top(size=size, group_privacy__in=[])
    assert len(result) == size


# pytest tests/tmain/repository/test_group_score.py::test_calc_bounds -v -s
@pytest.mark.parametrize(
    "position, window_offset, max_bound, asrt_lbound, asrt_ubound",
    (
        (2, 2, 10, 1, 5),
        (4, 2, 5, 1, 5),
        (2, 2, 3, 1, 3),
        (5, 10, 50, 1, 21),
    ),
)
def test_calc_bounds(position: int, window_offset: int, max_bound: int, asrt_lbound: int, asrt_ubound: int):
    lbound, ubound = calc_bounds(position, window_offset, max_bound)
    assert lbound == asrt_lbound
    assert ubound == asrt_ubound
