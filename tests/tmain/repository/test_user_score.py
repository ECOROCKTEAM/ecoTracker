import random
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from uuid import uuid4
from xml.dom.minidom import Entity

import pytest
from requests import delete
from sqlalchemy import func, select

from src.core.dto.user.score import UserRatingDTO
from src.core.enum.language import LanguageEnum
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.score.user import IRepositoryUserScore
from src.data.models.user.user import UserModel, UserScoreModel
from tests.dataloader import dataloader
from tests.utils import catchtime

USER_COUNT = 1_000
USER_ROWS_COUNT = 10


@asynccontextmanager
async def _arrange_func(dl: dataloader, user_count: int, user_rows_count: int) -> AsyncGenerator[str, None]:
    """Prepare score / rating
    return random user_id
    """
    user_models = []
    for _ in range(user_count):
        user = UserModel(
            id=str(uuid4()),
            username=str(uuid4()),
            active=True,
            language=LanguageEnum.EN,
        )
        user_models.append(user)
    dl.session.add_all(user_models)
    await dl.session.flush()

    score_models = []
    for user in user_models:
        for _ in range(user_rows_count):
            operation = random.choice([ScoreOperationEnum.MINUS, ScoreOperationEnum.PLUS])
            value = random.randint(50, 1000)
            score = UserScoreModel(user_id=user.id, operation=operation, value=value)
            score_models.append(score)
    dl.session.add_all(score_models)
    await dl.session.commit()

    stmt = select(func.count(UserScoreModel.id))
    count = await dl.session.scalar(stmt)
    assert count == user_count * user_rows_count
    user_id = random.choice(user_models).id
    yield user_id

    for score in score_models:
        await dl.session.delete(score)
    await dl.session.flush()
    for user in user_models:
        await dl.session.delete(user)
    await dl.session.commit()


@asynccontextmanager
async def _arrange_func_user_with_zero_rows_score(
    dl: dataloader,
) -> AsyncGenerator[str, None]:
    user = UserModel(
        id=str(uuid4()),
        username=str(uuid4()),
        active=True,
        language=LanguageEnum.EN,
    )
    dl.session.add(user)
    await dl.session.commit()

    yield user.id

    await dl.session.delete(user)
    await dl.session.commit()


async def _assert_func_score(dl: dataloader, user_id: str) -> int:
    stmt = select(UserScoreModel).where(UserScoreModel.user_id == user_id)
    raw_result_list = await dl.session.scalars(stmt)
    raw_result = UserRatingDTO(user_id=user_id, score=0, position=0)
    for obj in raw_result_list:
        if obj.operation == ScoreOperationEnum.PLUS:
            raw_result.score += obj.value
        elif obj.operation == ScoreOperationEnum.MINUS:
            raw_result.score -= obj.value
    return raw_result.score


# pytest tests/tmain/repository/test_user_score.py::test_get_rating -v -s
@pytest.mark.asyncio
async def test_get_rating(dl: dataloader, repo_user_score: IRepositoryUserScore):
    print()
    # Arrange
    async with _arrange_func(dl=dl, user_count=USER_COUNT, user_rows_count=USER_ROWS_COUNT) as user_id:
        # Act
        with catchtime("repo:"):
            result = await repo_user_score.get_rating(user_id=user_id)
        with catchtime("raw:"):
            score = await _assert_func_score(dl=dl, user_id=user_id)

    # Assert
    assert result.position > 0
    assert result.score == score
    assert result.user_id == user_id


# pytest tests/tmain/repository/test_user_score.py::test_get_score -v -s
@pytest.mark.asyncio
async def test_get_score(dl: dataloader, repo_user_score: IRepositoryUserScore):
    print()
    # Arrange
    async with _arrange_func(dl=dl, user_count=USER_COUNT, user_rows_count=USER_ROWS_COUNT) as user_id:
        # Act
        with catchtime("repo:"):
            result = await repo_user_score.get_score(user_id=user_id)
        with catchtime("raw:"):
            score = await _assert_func_score(dl=dl, user_id=user_id)

    # Assert
    assert result.score == score
    assert result.user_id == user_id


# pytest tests/tmain/repository/test_user_score.py::test_get_score_zero_rows_score -v -s
@pytest.mark.asyncio
async def test_get_score_zero_rows_score(dl: dataloader, repo_user_score: IRepositoryUserScore):
    print()
    # Arrange
    async with _arrange_func_user_with_zero_rows_score(
        dl=dl,
    ) as user_id:
        # Act
        with catchtime("repo:"):
            result = await repo_user_score.get_score(user_id=user_id)
        with catchtime("raw:"):
            score = await _assert_func_score(dl=dl, user_id=user_id)

    # Assert
    assert result.score == score
    assert result.score == 0
    assert result.user_id == user_id


# pytest tests/tmain/repository/test_user_score.py::test_get_score_not_found_user_fail -v -s
@pytest.mark.asyncio
async def test_get_score_not_found_user_fail(dl: dataloader, repo_user_score: IRepositoryUserScore):
    print()
    user_id = "1337"

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_user_score.get_score(user_id=user_id)


# pytest tests/tmain/repository/test_user_score.py::test_get_rating_not_found_user_fail -v -s
@pytest.mark.asyncio
async def test_get_rating_not_found_user_fail(dl: dataloader, repo_user_score: IRepositoryUserScore):
    print()
    user_id = "1337"

    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_user_score.get_rating(user_id=user_id)


# pytest tests/tmain/repository/test_user_score.py::test_get_rating_window -v -s
@pytest.mark.asyncio
async def test_get_rating_window(dl: dataloader, repo_user_score: IRepositoryUserScore):
    print()
    # Arrange
    size = 10
    async with _arrange_func(dl=dl, user_count=USER_COUNT, user_rows_count=USER_ROWS_COUNT) as user_id:
        # Act
        result = await repo_user_score.get_rating_window(size=size, user_id=user_id)

    # Assert
    user_id_set = {item.user_id for item in result}
    assert user_id in user_id_set
    assert len(result) == size
