import pytest

from src.core.dto.challenges.score import ScoreOperationValueDTO
from src.core.entity.user import User
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.usecases.score.user import (
    user_get_rating,
    user_get_score,
    user_score_increase,
)
from src.data.unit_of_work import SqlAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_user(pool, test_user: User, test_user_score):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = user_get_score.UserGetScoreUseCase(uow=uow)
    result = await uc(user=test_user)
    user = result.item
    assert user.user_id == test_user.id


@pytest.mark.asyncio
async def test_user_score_increase(pool, test_user: User, test_user_score):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = user_score_increase.UserChangeScoreUseCase(uow=uow)
    obj = ScoreOperationValueDTO(value=100, operation=ScoreOperationEnum.PLUS)
    result = await uc(user=test_user, obj=obj)
    user_score = result.item
    new_score = test_user_score.value
    new_score += obj.value
    assert user_score.user_id == test_user.id
    assert user_score.value == new_score
    assert user_score.operation == obj.operation
