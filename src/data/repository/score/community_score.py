from dataclasses import asdict

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.core.dto.community.score import (
    CommunityBoundOffsetDTO,
    CommunityOperationWithScoreDTO,
    CommunityRatingDTO,
    CommunityScoreDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.score import ScoreCommunity
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.score.community import IRepositoryCommunityScore
from src.data.models.community.community import CommunityScoreModel


def score_model_to_entity(model: CommunityScoreModel) -> ScoreCommunity:
    return ScoreCommunity(community_id=model.community_id, value=model.value, operation=model.operation)


class CommunityScoreRepository(IRepositoryCommunityScore):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def add(self, *, obj: CommunityOperationWithScoreDTO) -> ScoreCommunity:
        stmt = insert(CommunityScoreModel).values(**asdict(obj)).returning(CommunityScoreModel)
        result = await self.db_context.scalar(stmt)
        if not result:
            raise EntityNotFound()
        return score_model_to_entity(model=result)

    async def community_get(self, *, community_id: int) -> CommunityScoreDTO:
        stmt = select(CommunityScoreModel).where(CommunityScoreModel.community_id == community_id)
        result = await self.db_context.scalars(stmt)

        if not result:
            raise EntityNotFound()
        community_rating = CommunityScoreDTO(community_id=community_id, value=0)

        for obj in result:
            if obj.operation == ScoreOperationEnum.PLUS:
                community_rating.value += obj.value
            elif obj.operation == ScoreOperationEnum.MINUS:
                community_rating.value -= obj.value

        return community_rating

    async def community_rating(self, *, order_obj: MockObj, obj: CommunityBoundOffsetDTO):
        inner_stmt = select(
            func.row_number().over(order_by=CommunityScoreModel.value).label("position"),
            CommunityScoreModel.community_id,
            CommunityScoreModel.value,
        ).select_from(CommunityScoreModel)

        subquery = inner_stmt.subquery()
        alias = aliased(CommunityScoreModel, subquery)
        community_position_stmt = select(subquery).where(alias.community_id == obj.community_id)
        result = await self.db_context.execute(community_position_stmt)

        result_values = result.first()
        if not result_values:
            raise EntityNotFound()
        position, community_id, value = result_values

        community_position = CommunityRatingDTO(community_id=community_id, value=value, position=position)
        if (community_position.position - obj.bound_offset) <= 0:
            limit_obj = obj.bound_offset + community_position.position
            offset_obj = 0
        else:
            limit_obj = (obj.bound_offset * 2) + 1
            offset_obj = community_position.position - obj.bound_offset - 1

        stmt = (
            select(
                func.row_number().over(order_by=CommunityScoreModel.value).label("position"),
                CommunityScoreModel.community_id,
                CommunityScoreModel.value,
            )
            .select_from(CommunityScoreModel)
            .offset(offset_obj)
            .limit(limit_obj)
        )
        ex = await self.db_context.execute(stmt)
        result = ex.all()

        community_rating_list: list[CommunityRatingDTO] = []
        for community in result:
            position, community_id, value = community
            community_rating_list.append(CommunityRatingDTO(community_id=community_id, value=value, position=position))

        return community_rating_list
