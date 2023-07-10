import pytest_asyncio

from src.core.entity.score import ScoreCommunity
from src.core.enum.score.operation import ScoreOperationEnum
from tests.fixtures.const import (
    DEFAULT_TEST_CHALLENGE_SCORE,
    DEFAULT_TEST_USECASE_COMMUNITY_ID,
)


@pytest_asyncio.fixture
async def mock_community_score_add(monkeypatch) -> ScoreCommunity:
    async def f(*args, **kwargs) -> ScoreCommunity:
        return ScoreCommunity(
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            value=DEFAULT_TEST_CHALLENGE_SCORE,
            operation=ScoreOperationEnum.PLUS,
        )

    monkeypatch.setattr("src.data.repository.score.community_score.CommunityScoreRepository.add", f)
    return await f()
