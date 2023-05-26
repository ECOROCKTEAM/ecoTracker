from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

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


def community_position_to_entity(model) -> CommunityScoreDTO:
    return CommunityScoreDTO(
        community_id=model.community_id,
        value=model.value,
        position=model.position,
    )


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
        return score_model_to_entity(model=result)

    """ Как быть с тестами? Ждать дамба? Или вручную написать? Typehitting в функции к model аргументу """

    async def community_rating(self, *, order_obj: MockObj, obj: CommunityBoundOffsetDTO):
        inner_stmt = select(
            func.row_number().over(order_by=CommunityScoreModel.value),
            CommunityScoreModel.community_id,
            CommunityScoreModel.value,
        ).select_from(CommunityScoreModel)

        subquery = inner_stmt.subquery()
        alias = aliased(CommunityScoreModel, subquery)
        community_position_stmt = select(subquery).where(alias.community_id == obj.community_id)

        community_position = community_position_to_entity(model=community_position_stmt)

        if (community_position.position - obj.bound_offset) <= 0:
            limit_obj = obj.bound_offset + (obj.bound_offset - community_position.position) + 1
            offset_obj = 1
        else:
            limit_obj = obj.bound_offset * 2 + 1
            offset_obj = community_position.position - obj.bound_offset

        stmt = (
            select(
                func.row_number().over(order_by=CommunityScoreModel.value),
                CommunityScoreModel.community_id,
                CommunityScoreModel.value,
            )
            .select_from(CommunityScoreModel)
            .offset(offset_obj)
            .limit(limit_obj)
        )

        result = await self.db_context.scalars(stmt)
        return [community_position_to_entity(model=model) for model in result]
