import pytest_asyncio

from src.core.entity.score import ScoreGroup
from src.core.enum.score.operation import ScoreOperationEnum
from tests.fixtures.const import (
    DEFAULT_TEST_CHALLENGE_SCORE,
    DEFAULT_TEST_USECASE_GROUP_ID,
)


@pytest_asyncio.fixture
async def mock_group_score_add(monkeypatch) -> ScoreGroup:
    async def f(*args, **kwargs) -> ScoreGroup:
        return ScoreGroup(
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            value=DEFAULT_TEST_CHALLENGE_SCORE,
            operation=ScoreOperationEnum.PLUS,
            mission_totaly_completed=1,
        )

    monkeypatch.setattr("src.data.repository.score.group_score.GroupScoreRepository.add", f)
    return await f()
