import warnings
from dataclasses import asdict

from sqlalchemy import Integer, case, func, insert, literal, select
from sqlalchemy.exc import SAWarning
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.user.score import (
    OperationWithScoreUserDTO,
    UserRatingDTO,
    UserScoreDTO,
)
from src.core.entity.score import ScoreUser
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.score.user import IRepositoryUserScore
from src.data.models.user.user import UserModel, UserScoreModel

_SCORE_RAW_TABLE_SUBQ = (
    select(
        UserScoreModel.user_id.label("user_id"),
        func.sum(
            case(
                (
                    UserScoreModel.operation == ScoreOperationEnum.MINUS,
                    UserScoreModel.value * -1,
                ),
                else_=UserScoreModel.value,
            ),
        ).label("score"),
    )
    .group_by(UserScoreModel.user_id)
    .subquery("score_raw_table")
)

_SCORE_TABLE_SUBQ = (
    select(
        UserModel.id.label("user_id"),
        func.coalesce(_SCORE_RAW_TABLE_SUBQ.c.score, 0).label("score"),
    )
    .outerjoin(
        _SCORE_RAW_TABLE_SUBQ,
        UserModel.id.label("user_id") == _SCORE_RAW_TABLE_SUBQ.c.user_id,
    )
    .order_by(_SCORE_RAW_TABLE_SUBQ.c.score.desc())
    .subquery("score_table")
)

_RATING_TABLE_CTE = select(
    _SCORE_TABLE_SUBQ.c.user_id.label("user_id"),
    _SCORE_TABLE_SUBQ.c.score.label("score"),
    func.row_number().over(order_by=_SCORE_TABLE_SUBQ.c.score.desc()).label("position"),
).cte("rating_table_cte")


_WINDOW_CONSTRAINT_CTE = (
    select(
        func.max(_RATING_TABLE_CTE.c.position).label("position_max"),
        func.min(_RATING_TABLE_CTE.c.position).label("position_min"),
    )
    .select_from(_RATING_TABLE_CTE)
    .cte("window_constraint_cte")
)


_RATING_ONE_USER_STMT = select(
    _RATING_TABLE_CTE.c.user_id.label("user_id"),
    _RATING_TABLE_CTE.c.score.label("score"),
    _RATING_TABLE_CTE.c.position.label("position"),
).select_from(_RATING_TABLE_CTE)


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
        stmt = (
            select(
                _SCORE_TABLE_SUBQ.c.user_id.label("user_id"),
                _SCORE_TABLE_SUBQ.c.score.label("score"),
            )
            .select_from(_SCORE_TABLE_SUBQ)
            .where(_SCORE_TABLE_SUBQ.c.user_id == user_id)
        )
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
        stmt = _RATING_ONE_USER_STMT
        stmt = stmt.where(_RATING_TABLE_CTE.c.user_id == user_id)
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
        size: int,
        user_id: int | None = None,
    ) -> list[UserRatingDTO]:
        half_size = int(size / 2)
        _all_contraint_cte = (
            select(
                _RATING_TABLE_CTE.c.position.label("position"),
                _WINDOW_CONSTRAINT_CTE.c.position_max.label("position_max"),
                _WINDOW_CONSTRAINT_CTE.c.position_min.label("position_min"),
                literal(f"{half_size}").cast(Integer).label("window_size"),
            )
            .select_from(_RATING_TABLE_CTE)
            .where(_RATING_TABLE_CTE.c.user_id == user_id)
            .add_cte(_WINDOW_CONSTRAINT_CTE)
            .cte("contraint_all_cte")
        )
        _bound_cte = (
            select(
                _RATING_TABLE_CTE.c.position.label("position"),
                func.lag(
                    _RATING_TABLE_CTE.c.position,
                    _all_contraint_cte.c.window_size.label("window_size"),
                    _all_contraint_cte.c.position_min.label("position_min"),
                )
                .over()
                .label("lbound"),
                func.lead(
                    _RATING_TABLE_CTE.c.position,
                    _all_contraint_cte.c.window_size.label("window_size") - 1,
                    _all_contraint_cte.c.position_max.label("position_max"),
                )
                .over()
                .label("ubound"),
            )
            .select_from(_all_contraint_cte)
            .cte("bound_cte")
        )
        stmt = (
            select(
                _RATING_TABLE_CTE.c.user_id,
                _RATING_TABLE_CTE.c.score,
                _RATING_TABLE_CTE.c.position,
            )
            .add_cte(_RATING_TABLE_CTE)
            .join(_bound_cte, _bound_cte.c.position == _RATING_TABLE_CTE.c.position)
            .join(
                _all_contraint_cte,
                _all_contraint_cte.c.position.between(_bound_cte.c.lbound, _bound_cte.c.ubound),
            )
        )

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=SAWarning)
            coro = await self.db_context.execute(stmt)
        result = coro.all()
        if len(result) == 0:
            raise EntityNotFound(msg=f"User={user_id} not found")
        items = [
            UserRatingDTO(user_id=_user_id, score=score, position=position) for _user_id, score, position in result
        ]
        return items
