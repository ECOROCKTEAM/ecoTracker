from dataclasses import asdict

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.group.score import AddScoreGroupDTO, GroupRatingDTO, GroupScoreDTO
from src.core.entity.score import ScoreGroup
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.score.group import IRepositoryGroupScore
from src.data.models.group.group import GroupScoreModel
from src.data.repository.score.qbuilder import (
    build_rating_table_stmt,
    build_score_table_stmt,
    showq,
)
from src.data.repository.score.utils import calc_bounds


def score_model_to_entity(model: GroupScoreModel) -> ScoreGroup:
    return ScoreGroup(group_id=model.group_id, value=model.value, operation=model.operation)


class RepositoryGroupScore(IRepositoryGroupScore):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def add(self, *, obj: AddScoreGroupDTO) -> ScoreGroup:
        stmt = insert(GroupScoreModel).values(**asdict(obj)).returning(GroupScoreModel)
        result = await self.db_context.scalar(stmt)
        if not result:
            raise EntityNotFound(msg=f"Group={obj.group_id} not found")
        return score_model_to_entity(model=result)

    async def get_score(self, *, group_id: int) -> GroupScoreDTO:
        stmt = build_score_table_stmt(model=GroupScoreModel, target_id=group_id)
        coro = await self.db_context.execute(stmt)
        result = coro.one_or_none()
        if not result:
            raise EntityNotFound(msg=f"Group={group_id} not found")
        _group_id, score = result
        assert _group_id == group_id
        return GroupScoreDTO(group_id=_group_id, score=score)

    async def get_rating(
        self,
        *,
        group_id: int,
    ) -> GroupRatingDTO:
        stmt = build_rating_table_stmt(model=GroupScoreModel, target_id=group_id)
        coro = await self.db_context.execute(stmt)
        result = coro.one_or_none()
        if result is None:
            raise EntityNotFound(msg=f"Group={group_id} not found")
        _group_id, score, position = result
        assert group_id == _group_id
        return GroupRatingDTO(group_id=_group_id, score=score, position=position)

    async def get_rating_window(
        self, *, window_offset: int, group_id: int, group_privacy__in: list[GroupPrivacyEnum]
    ) -> list[GroupRatingDTO]:
        stmt = build_rating_table_stmt(model=GroupScoreModel, target_id=group_id, with_max_bound=True)
        showq(stmt)
        coro = await self.db_context.execute(stmt)
        result = coro.one_or_none()
        if result is None:
            raise EntityNotFound(msg=f"Group={group_id} not found")
        _group_id, _, position, max_position = result
        assert group_id == _group_id
        lbound, ubound = calc_bounds(
            position=position, window_offset=window_offset, max_bound=max_position, min_bound=1
        )
        stmt = build_rating_table_stmt(model=GroupScoreModel, lbound=lbound, ubound=ubound)
        coro = await self.db_context.execute(stmt)
        result = coro.all()
        items = [
            GroupRatingDTO(group_id=_group_id, score=score, position=position) for _group_id, score, position in result
        ]
        return items

    async def get_rating_top(self, *, size: int, group_privacy__in: list[GroupPrivacyEnum]) -> list[GroupRatingDTO]:
        stmt = build_rating_table_stmt(model=GroupScoreModel, limit=size)
        coro = await self.db_context.execute(stmt)
        result = coro.all()
        items = [
            GroupRatingDTO(group_id=_group_id, score=score, position=position) for _group_id, score, position in result
        ]
        return items
