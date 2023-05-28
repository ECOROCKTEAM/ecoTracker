import pytest

from src.core.dto.mock import MockObj
from src.core.entity.community import Community
from src.core.usecases.score.community import community_get_rating, community_get_score
from src.data.unit_of_work import SqlAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_score_get(pool, test_score_community, test_community, test_user):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = community_get_score.CommunityGetScoreUseCase(uow=uow)
    result = await uc(community=test_community, user=test_user)
    score = result.item
    assert score.community_id == test_community.id
    assert test_score_community.value == score.value


@pytest.mark.asyncio
async def test_community_rating(
    pool,
    test_user,
    test_community_score,
    community_for_rating: Community,
    test_community_list,
):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = community_get_rating.CommunityGetRatingUseCase(uow=uow)
    result = await uc(user=test_user, community_id=community_for_rating.id, order_obj=MockObj(), bound_offset=4)
    community_rating = result.item
    for community in community_rating:
        assert isinstance(community.community_id, int)
        assert isinstance(community.position, int)
        assert isinstance(community.value, int)
        # Какие тут можно добавить проверки?
