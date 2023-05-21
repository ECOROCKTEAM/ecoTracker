import pytest

from src.core.dto.challenges.score import ScoreOperationValueDTO
from src.core.dto.community.score import CommunityOperationWithScoreDTO
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.usecases.score.community import (
    community_get_rating,
    community_get_score,
    communnity_score_increase,
)
from src.data.unit_of_work import SqlAlchemyUnitOfWork

""" 
Если 2 теста в работе - ошибка: накладываются друг на друга и не проходит проверка по score.value.
Спросить на созвоне
"""

# @pytest.mark.asyncio
# async def test_score_increase(pool, test_score_community, test_community, test_user, test_user_community):
#     obj = ScoreOperationValueDTO(
#         value=100,
#         operation=ScoreOperationEnum.PLUS
#     )
#     uow = SqlAlchemyUnitOfWork(pool)
#     uc = communnity_score_increase.CommunityChangeRatingUseCase(uow=uow)
#     result = await uc(
#         community=test_community,
#         user=test_user,
#         obj=obj,
#     )
#     com_score = result.item
#     new_score = test_score_community.value + obj.value
#     assert com_score.community_id == test_community.id
#     assert com_score.value == new_score


@pytest.mark.asyncio
async def test_score_get(pool, test_score_community, test_community, test_user):
    uow = SqlAlchemyUnitOfWork(pool)
    uc = community_get_score.CommunityGetScoreUseCase(uow=uow)
    result = await uc(community=test_community, user=test_user)
    score = result.item
    assert score.community_id == test_community.id
    assert test_score_community.value == score.value
