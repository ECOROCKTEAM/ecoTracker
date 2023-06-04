import pytest

from src.core.dto.mock import MockObj
from src.core.entity.user import User
from src.core.usecases.score.user import user_get_rating, user_get_score
from src.data.unit_of_work import SqlAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_user(pool, test_user: User, user_operations_list):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = user_get_score.UserGetScoreUseCase(uow=uow)
    result = await uc(user=test_user)
    user = result.item
    assert user.user_id == test_user.id


@pytest.mark.asyncio
async def test_user_rating(
    pool,
    test_users,
    test_users_scores,
    test_user_for_rating: User,
):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = user_get_rating.UserGetRatingUseCase(uow=uow)
    result = await uc(user=test_user_for_rating, order_obj=MockObj(), bound_offset=4)
    users_rating = result.items
    for user in users_rating:
        assert isinstance(user.position, int)
        assert isinstance(user.user_id, int)
        assert isinstance(user.value, int)
        # хз что тут проверять...
