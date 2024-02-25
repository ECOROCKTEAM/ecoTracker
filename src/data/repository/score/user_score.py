from dataclasses import asdict

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.user.score import (
    OperationWithScoreUserDTO,
    UserRatingDTO,
    UserScoreDTO,
)
from src.core.entity.score import ScoreUser
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.score.user import IRepositoryUserScore
from src.data.models.user.user import UserScoreModel
from src.data.repository.score.qbuilder import (
    build_rating_table_stmt,
    build_score_table_stmt,
)


def calc_bounds(position: int, window_offset: int, max_bound: int, min_bound: int = 1) -> tuple[int, int]:
    ubound = position + window_offset
    lbound = position - window_offset

    # check lboud
    if lbound <= 0:
        ubound += min_bound - lbound
        lbound = min_bound

    # check ubound
    if ubound > max_bound and lbound == min_bound:
        ubound = max_bound
    elif ubound > max_bound and lbound - (ubound - max_bound) >= min_bound:
        lbound = lbound - abs(max_bound - ubound)
        ubound = max_bound

    return lbound, ubound


def score_model_to_entity(model: UserScoreModel) -> ScoreUser:
    return ScoreUser(
        user_id=model.user_id,
        value=model.value,
        operation=model.operation,
    )


class RepositoryUserScore(IRepositoryUserScore):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def add(self, *, obj: OperationWithScoreUserDTO) -> ScoreUser:
        stmt = insert(UserScoreModel).values(**asdict(obj)).returning(UserScoreModel)
        result = await self.db_context.scalar(stmt)
        if not result:
            raise EntityNotFound(msg=f"User={obj.user_id} not found")
        return score_model_to_entity(model=result)

    async def get_score(self, *, user_id: str) -> UserScoreDTO:
        stmt = build_score_table_stmt(model=UserScoreModel, target_id=user_id)
        coro = await self.db_context.execute(stmt)
        result = coro.one_or_none()
        if not result:
            raise EntityNotFound(msg=f"User={user_id} not found")
        _user_id, score = result
        return UserScoreDTO(user_id=_user_id, score=score)

    async def get_rating(
        self,
        *,
        user_id: str,
    ) -> UserRatingDTO:
        stmt = build_rating_table_stmt(model=UserScoreModel, target_id=user_id)
        coro = await self.db_context.execute(stmt)
        result = coro.one_or_none()
        if result is None:
            raise EntityNotFound(msg=f"User={user_id} not found")
        _user_id, score, position = result
        assert user_id == _user_id
        return UserRatingDTO(user_id=_user_id, score=score, position=position)

    async def get_rating_window(
        self,
        *,
        window_offset: int,
        user_id: str,
    ) -> list[UserRatingDTO]:
        stmt = build_rating_table_stmt(model=UserScoreModel, target_id=user_id, with_max_bound=True)
        coro = await self.db_context.execute(stmt)
        result = coro.one_or_none()
        if result is None:
            raise EntityNotFound(msg=f"User={user_id} not found")
        _user_id, _, position, max_position = result
        assert user_id == _user_id
        lbound, ubound = calc_bounds(
            position=position, window_offset=window_offset, max_bound=max_position, min_bound=1
        )
        stmt = build_rating_table_stmt(model=UserScoreModel, lbound=lbound, ubound=ubound)
        coro = await self.db_context.execute(stmt)
        result = coro.all()
        items = [
            UserRatingDTO(user_id=_user_id, score=score, position=position) for _user_id, score, position in result
        ]
        return items

    async def get_rating_top(self, *, size: int) -> list[UserRatingDTO]:
        stmt = build_rating_table_stmt(model=UserScoreModel, limit=size)
        coro = await self.db_context.execute(stmt)
        result = coro.all()
        items = [
            UserRatingDTO(user_id=_user_id, score=score, position=position) for _user_id, score, position in result
        ]
        return items
