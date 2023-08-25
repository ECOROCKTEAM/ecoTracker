from dataclasses import asdict

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.core.dto.group.score import (
    GroupBoundOffsetDTO,
    GroupOperationWithScoreDTO,
    GroupRatingDTO,
    GroupScoreDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.score import ScoreGroup
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.score.group import IRepositoryGroupScore
from src.data.models.group.group import GroupScoreModel


def score_model_to_entity(model: GroupScoreModel) -> ScoreGroup:
    return ScoreGroup(group_id=model.group_id, value=model.value, operation=model.operation)


class GroupScoreRepository(IRepositoryGroupScore):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def add(self, *, obj: GroupOperationWithScoreDTO) -> ScoreGroup:
        stmt = insert(GroupScoreModel).values(**asdict(obj)).returning(GroupScoreModel)
        result = await self.db_context.scalar(stmt)
        if not result:
            raise EntityNotFound(msg=f"group={obj.group_id} not found")
        return score_model_to_entity(model=result)

    async def group_get(self, *, group_id: int) -> GroupScoreDTO:
        stmt = select(GroupScoreModel).where(GroupScoreModel.group_id == group_id)
        result = await self.db_context.scalars(stmt)

        if not result:
            raise EntityNotFound(msg=f"group={group_id} not found")
        group_rating = GroupScoreDTO(group_id=group_id, value=0)

        for obj in result:
            if obj.operation == ScoreOperationEnum.PLUS:
                group_rating.value += obj.value
            elif obj.operation == ScoreOperationEnum.MINUS:
                group_rating.value -= obj.value

        return group_rating

    async def group_rating(self, *, order_obj: MockObj, obj: GroupBoundOffsetDTO):
        inner_stmt = select(
            func.row_number().over(order_by=GroupScoreModel.value).label("position"),
            GroupScoreModel.group_id,
            GroupScoreModel.value,
        ).select_from(GroupScoreModel)

        subquery = inner_stmt.subquery()
        alias = aliased(GroupScoreModel, subquery)
        group_position_stmt = select(subquery).where(alias.group_id == obj.group_id)
        result = await self.db_context.execute(group_position_stmt)

        result_values = result.first()
        if not result_values:
            raise EntityNotFound(msg=f"group={obj.group_id} not found")
        position, group_id, value = result_values

        group_position = GroupRatingDTO(group_id=group_id, value=value, position=position)
        if (group_position.position - obj.bound_offset) <= 0:
            limit_obj = obj.bound_offset + group_position.position
            offset_obj = 0
        else:
            limit_obj = (obj.bound_offset * 2) + 1
            offset_obj = group_position.position - obj.bound_offset - 1

        stmt = (
            select(
                func.row_number().over(order_by=GroupScoreModel.value).label("position"),
                GroupScoreModel.group_id,
                GroupScoreModel.value,
            )
            .select_from(GroupScoreModel)
            .offset(offset_obj)
            .limit(limit_obj)
        )
        ex = await self.db_context.execute(stmt)
        result = ex.all()

        group_rating_list: list[GroupRatingDTO] = []
        for group in result:
            position, group_id, value = group
            group_rating_list.append(GroupRatingDTO(group_id=group_id, value=value, position=position))

        return group_rating_list
