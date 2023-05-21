from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.community.score import (
    CommunityBoundOffsetDTO,
    CommunityOperationWithScoreDTO,
    CommunityScoreDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.score import ScoreCommunity
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.score.community import IRepositoryCommunityScore
from src.data.models.community.community import CommunityScoreModel
from src.data.repository.score.user_score import rating_calculation
from src.utils import as_dict_skip_none


def score_model_to_entity(model: CommunityScoreModel) -> ScoreCommunity:
    return ScoreCommunity(community_id=model.community_id, value=model.value, operation=model.operation)


class CommunityScoreRepository(IRepositoryCommunityScore):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def change(self, *, obj: CommunityOperationWithScoreDTO) -> ScoreCommunity:
        stmt = select(CommunityScoreModel).where(CommunityScoreModel.community_id == obj.community_id)
        result = await self.db_context.scalar(stmt)
        if not result:
            raise EntityNotFound()
        new_score = rating_calculation(current_value=result.value, operated_value=obj.value, operation=obj.operation)
        new_obj = ScoreCommunity(
            community_id=obj.community_id,
            value=new_score,
            operation=obj.operation,
        )
        new_score_stmt = (
            update(CommunityScoreModel)
            .where(CommunityScoreModel.community_id == obj.community_id)
            .values(**as_dict_skip_none(new_obj))
            .returning(CommunityScoreModel)
        )
        result = await self.db_context.scalar(new_score_stmt)
        if not result:
            raise EntityNotFound()
        return score_model_to_entity(model=result)

    async def community_get(self, *, community_id: int) -> ScoreCommunity:
        stmt = select(CommunityScoreModel).where(CommunityScoreModel.community_id == community_id)
        result = await self.db_context.scalar(stmt)
        if not result:
            raise EntityNotFound()
        print(result.value)
        return score_model_to_entity(model=result)

    async def community_rating(
        self, *, order_obj: MockObj, obj: CommunityBoundOffsetDTO | None = None
    ) -> dict[int, CommunityScoreDTO]:
        return await super().community_rating(order_obj=order_obj, obj=obj)
