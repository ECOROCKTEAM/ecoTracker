import pytest_asyncio

from src.core.entity.score import ScoreUser
from src.core.enum.score.operation import ScoreOperationEnum
from tests.fixtures.const import (
    DEFAULT_TEST_CHALLENGE_SCORE,
    DEFAULT_TEST_USECASE_USER_ID,
)


@pytest_asyncio.fixture
async def mock_user_score_add(monkeypatch) -> ScoreUser:
    async def f(*args, **kwargs) -> ScoreUser:
        return ScoreUser(
            user_id=DEFAULT_TEST_USECASE_USER_ID, value=DEFAULT_TEST_CHALLENGE_SCORE, operation=ScoreOperationEnum.PLUS
        )

    monkeypatch.setattr("src.data.repository.score.user_score.UserScoreRepository.add", f)
    return await f()
